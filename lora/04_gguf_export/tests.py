import os
import tempfile

import torch
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM, AutoTokenizer

# Use a small model for testing
TEST_MODEL = "Qwen/Qwen2.5-0.5B"

# Path to llama.cpp (can be overridden via environment variable)
LLAMA_CPP_PATH = os.environ.get("LLAMA_CPP_PATH", "~/llama.cpp")


def check_llama_cpp():
    """Check if llama.cpp is available and return the path, or None if not found."""
    llama_cpp = os.path.expanduser(LLAMA_CPP_PATH)
    convert_script = os.path.join(llama_cpp, "convert_hf_to_gguf.py")

    if not os.path.exists(convert_script):
        return None

    # Check for quantize binary
    for path in [
        os.path.join(llama_cpp, "build", "bin", "llama-quantize"),
        os.path.join(llama_cpp, "llama-quantize"),
        os.path.join(llama_cpp, "quantize"),
    ]:
        if os.path.exists(path):
            return llama_cpp

    return None


def create_test_adapters(output_dir: str):
    """Create a simple LoRA adapter for testing."""
    model = AutoModelForCausalLM.from_pretrained(TEST_MODEL)
    tokenizer = AutoTokenizer.from_pretrained(TEST_MODEL)

    lora_config = LoraConfig(
        r=8,
        lora_alpha=16,
        target_modules=["q_proj", "v_proj"],
        task_type="CAUSAL_LM",
    )

    peft_model = get_peft_model(model, lora_config)

    # Save adapters
    peft_model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)

    return peft_model


def run_tests(func):
    """Test suite for GGUF export exercise."""
    print(f"Running tests for {func.__name__}...\n")

    llama_cpp = check_llama_cpp()
    if llama_cpp is None:
        print("=" * 60)
        print("SKIPPING TESTS: llama.cpp not found")
        print()
        print("To run these tests, install llama.cpp:")
        print(f"  git clone https://github.com/ggml-org/llama.cpp {LLAMA_CPP_PATH}")
        print(f"  cd {LLAMA_CPP_PATH} && make")
        print()
        print("Or set LLAMA_CPP_PATH environment variable to your installation.")
        print("=" * 60)
        return

    print(f"Using llama.cpp at: {llama_cpp}")

    # Test 1: Returns a valid path to .gguf file
    print("\nTest 1: Checking return value...")
    with tempfile.TemporaryDirectory() as tmpdir:
        adapter_path = os.path.join(tmpdir, "adapters")
        create_test_adapters(adapter_path)

        output_path = os.path.join(tmpdir, "model")

        result = func(
            model_name=TEST_MODEL,
            adapter_path=adapter_path,
            output_path=output_path,
            llama_cpp_path=llama_cpp,
            quantization="q4_k_m",
        )

        assert result is not None, "Test 1 failed: function should return a path"
        assert isinstance(result, str), (
            f"Test 1 failed: should return str, got {type(result).__name__}"
        )
        assert result.endswith(".gguf"), (
            f"Test 1 failed: path should end with .gguf, got {result}"
        )
        print(f"Test 1 passed: Returns valid path ({os.path.basename(result)})")

    # Test 2: GGUF file exists and has reasonable size
    print("Test 2: Checking GGUF file exists...")
    with tempfile.TemporaryDirectory() as tmpdir:
        adapter_path = os.path.join(tmpdir, "adapters")
        create_test_adapters(adapter_path)

        output_path = os.path.join(tmpdir, "model")

        result = func(
            model_name=TEST_MODEL,
            adapter_path=adapter_path,
            output_path=output_path,
            llama_cpp_path=llama_cpp,
            quantization="q4_k_m",
        )

        assert os.path.exists(result), f"Test 2 failed: GGUF file not found at {result}"

        file_size = os.path.getsize(result)
        assert file_size > 1_000_000, (  # Should be at least 1MB for a real model
            f"Test 2 failed: GGUF file too small ({file_size} bytes)"
        )
        size_mb = file_size / (1024 * 1024)
        print(f"Test 2 passed: GGUF file exists ({size_mb:.1f} MB)")

    # Test 3: Quantized file is smaller than F16
    print("Test 3: Checking quantization reduces size...")
    with tempfile.TemporaryDirectory() as tmpdir:
        adapter_path = os.path.join(tmpdir, "adapters")
        create_test_adapters(adapter_path)

        # Export F16
        output_f16 = os.path.join(tmpdir, "model_f16")
        result_f16 = func(
            model_name=TEST_MODEL,
            adapter_path=adapter_path,
            output_path=output_f16,
            llama_cpp_path=llama_cpp,
            quantization="f16",
        )

        # Export Q4_K_M
        output_q4 = os.path.join(tmpdir, "model_q4")
        result_q4 = func(
            model_name=TEST_MODEL,
            adapter_path=adapter_path,
            output_path=output_q4,
            llama_cpp_path=llama_cpp,
            quantization="q4_k_m",
        )

        size_f16 = os.path.getsize(result_f16)
        size_q4 = os.path.getsize(result_q4)

        assert size_q4 < size_f16, (
            f"Test 3 failed: Q4_K_M ({size_q4}) should be smaller than F16 ({size_f16})"
        )

        reduction = (1 - size_q4 / size_f16) * 100
        print(f"Test 3 passed: Q4_K_M is {reduction:.0f}% smaller than F16")

    # Test 4: Merged model produces same output as adapter model
    print("Test 4: Checking merge preserves model behavior...")
    with tempfile.TemporaryDirectory() as tmpdir:
        adapter_path = os.path.join(tmpdir, "adapters")
        peft_model = create_test_adapters(adapter_path)

        # Get output from adapter model
        tokenizer = AutoTokenizer.from_pretrained(TEST_MODEL)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token

        test_input = tokenizer("Hello", return_tensors="pt")
        device = next(peft_model.parameters()).device
        test_input = {k: v.to(device) for k, v in test_input.items()}

        with torch.no_grad():
            adapter_output = peft_model(**test_input).logits

        # Load base model and merge adapters (same as export does internally)
        base_model = AutoModelForCausalLM.from_pretrained(TEST_MODEL)
        from peft import PeftModel

        loaded_peft = PeftModel.from_pretrained(base_model, adapter_path)
        merged_model = loaded_peft.merge_and_unload()

        with torch.no_grad():
            merged_output = merged_model(**test_input).logits

        # Check outputs are close
        diff = (adapter_output - merged_output).abs().max().item()
        assert diff < 1e-4, (
            f"Test 4 failed: merged model output differs from adapter model (max diff: {diff})"
        )
        print(
            f"Test 4 passed: Merged model matches adapter model (max diff: {diff:.2e})"
        )

    print("\nAll tests passed!")
