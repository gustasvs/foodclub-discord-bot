import soundfile as sf
import numpy as np
import discord
from utils.transcription.simple_google_transcriber import google_lv_transcriber
from utils.helpers import format_error_message

# from transcriber_helpers import get_pipe
# from utils.transcription.transcriber_helpers import get_pipe


# pipe = get_pipe()

# def transcribe_audio(audio_path, language="english"):
#     audio_data, sample_rate = sf.read(audio_path)
#     if audio_data.ndim > 1:
#         audio_data = np.mean(audio_data, axis=1)
#     result = pipe(audio_data, generate_kwargs={"language": language})
#     print(result["text"])
#     return result

async def handle_audio_attachment(message):
    for attachment in message.attachments:
        if attachment.content_type.startswith('audio/') or attachment.filename.endswith(('.wav', '.mp3', '.ogg')):
            await message.channel.typing()
            temp_path = f'temp/temp_{attachment.filename}'
            await attachment.save(temp_path)
            print(f'Received and saved an audio file: {attachment.filename}')
            # transcription = transcribe_audio(temp_path, "latvian")
            transcription, transcription_success = google_lv_transcriber(temp_path)
            if not transcription_success:
                await message.channel.send(format_error_message(transcription))
                return True
            transcription_message = f"Transcription provided using Google Speech Recognition for lv-LV:\n```{transcription}```"
            embed = discord.Embed(
                title="Transcription",
                description=transcription_message,
                color=0x00ff00
            )
            await message.channel.send(embed=embed)
            return True
    return False


# if __name__ == "__main__":
#     filename = "sample.ogg"
#     transcribe_audio(filename, "latvian")

# async def handle_audio_attachment(message):
#     for attachment in message.attachments:
#         if attachment.content_type.startswith('audio/') or attachment.filename.endswith(('.wav', '.mp3', '.ogg')):
#             await message.channel.send("Transcription is not available at the moment. Please try again later.")
#             return True
#     return False