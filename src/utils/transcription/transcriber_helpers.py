import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

def get_pipe():
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    # TODO for best results use whisper-large-v3, but it requires a lot of memory
    # model_id = "openai/whisper-large-v3"
    # model_id = "facebook/s2t-large-librispeech-asr"
    model_id = "openai/whisper-medium"

    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
    )
    model.to(device)

    processor = AutoProcessor.from_pretrained(model_id)

    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        max_new_tokens=128, # this is the maximum number of tokens that can be generated in a single call to the model
        chunk_length_s=60,
        batch_size=16,
        return_timestamps=True,
        torch_dtype=torch_dtype,
        device=device,
    )

    return pipe