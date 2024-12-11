from __future__ import annotations

import asyncio
import json
import logging
# import os
import uuid
from dataclasses import asdict, dataclass
from typing import Any, Dict, Literal

from livekit import rtc
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    WorkerOptions,
    WorkerType,
    cli,
    llm,
)
from livekit.agents.multimodal import MultimodalAgent
from livekit.plugins import openai

logger = logging.getLogger("my-worker")
logger.setLevel(logging.INFO)


# Set environment variables
# os.environ["LIVEKIT_URL"] = "wss://kvitka-polonyna-g7za18xm.livekit.cloud"
# os.environ["LIVEKIT_API_KEY"] = "APIpvgqjCvqxeMr"
# os.environ["LIVEKIT_API_SECRET"] = "2Hse4qYdbIfpPFRsSY6q0aoMf6LShqjQsDbAZtPfEMvD"

# Define a function context class with your function(s)
class AssistantFnc(llm.FunctionContext):
    @llm.ai_callable()
    async def get_water_info(self):
        """
        Called when the user asks about water. This function will return
        information about water. The LLM can call this function to retrieve details about
        different types of water, their properties, and general facts.
        """
        logger.info(f"Getting info about water")
        return (
            "'Kvitka Polonyny' is the only resort in Transcarpathia with three times more balneological healing options compared to other health resorts.\n"
            "This is due to its powerful hydro-mineral resources, offering three types of mineral water: \"Luzhanska-4\", \"Luzhanska-7\", and \"Polyana Kvasova\".\n"
            "Mineral water is directly supplied from the source to the pump room, bath department, and other procedure rooms.\n\n"
            "1. **Luzhanska-4**:\n"
            "   - Origin: Originally named \"Margit\", this low-mineralized bicarbonate sodium water is known for its ability to neutralize stomach acidity, relieve indigestion, and improve bile flow.\n"
            "   - Uses: Treats gastrointestinal issues, kidney diseases, and enhances cardiovascular function through external carbonated mineral baths.\n\n"
            "2. **Luzhanska-7**:\n"
            "   - Highlights: This medium-mineralized water contains biologically active calcium and metasilicic acid. It supports fat metabolism, acts as an expectorant, and provides antioxidant benefits.\n"
            "   - Uses: Beneficial for liver diseases, diabetes, and respiratory conditions. Suitable for both healthy individuals and children.\n\n"
            "3. **Polyana Kvasova**:\n"
            "   - Features: Formed at depths of 300-500 meters, making it highly protected from contamination. Known as the \"queen of lithium bicarbonate alkaline mineral waters\".\n"
            "   - Uses: Highly effective for treating ulcers, gastritis, and conditions with increased acidity. Its bicarbonate content exceeds that of popular \"Borjomi\", making it superior for neutralizing acidity.\n\n"
            "These mineral waters are also used in therapies such as natural carbonated baths, mineral water inhalations, and gynecological irrigation."
        )

    @llm.ai_callable()
    async def get_healthcare_procedures(self):
        """
        Called when the user asks about procedures. This function will return
        information about the sanatorium's healthcare procedures.
        """
        logger.info(f"Getting info about procedures")
        return (
            "Here is information about the sanatorium's healthcare procedures:\n\n"
            "1. **Balneotherapy**:\n"
            "   - Description: Therapeutic use of mineral water baths for conditions like arthritis, cardiovascular issues, and stress disorders.\n"
            "   - Benefits: Improves joint mobility, enhances cardiovascular function, and reduces chronic pain.\n"
            "   - Applications: Thermal Baths, Mineral Drinking Cure.\n\n"
            "2. **Physiotherapy**:\n"
            "   - Description: Physical methods like exercises and modern technology to restore movement and function.\n"
            "   - Benefits: Improves mobility, relieves chronic pain, and enhances strength and endurance.\n"
            "   - Applications: Electrotherapy, Therapeutic Exercises.\n\n"
            "3. **Mud Therapy (Peloid Therapy)**:\n"
            "   - Description: Application of therapeutic mud to reduce inflammation and promote healing.\n"
            "   - Benefits: Relieves pain, improves circulation, and accelerates tissue regeneration.\n"
            "   - Applications: Direct Application, Mud Baths.\n\n"
            "4. **Rehabilitation**:\n"
            "   - Description: Comprehensive programs for recovery from surgeries, injuries, or chronic illnesses.\n"
            "   - Benefits: Restores functional independence, enhances quality of life, and reduces risk of complications.\n"
            "   - Applications: Post-surgical Rehabilitation, Neurological Rehabilitation."
        )

    @llm.ai_callable()
    async def get_doctors_info(self):
        """
        Called when the user asks about available doctors. This function will return
        information about the doctors at the sanatorium.
        """
        logger.info(f"Getting info about doctors")
        return (
            "Here is a list of available doctors at the sanatorium:\n\n"
            "1. **Doctor Olena Kovalenko**\n"
            "   - Specialization: Balneologist\n"
            "   - Phone: +380 50 123 4567\n"
            "   - Work Hours: Monday - Friday, 9:00 - 17:00\n\n"
            "2. **Doctor Ivan Petrov**\n"
            "   - Specialization: Physiotherapist\n"
            "   - Phone: +380 67 234 5678\n"
            "   - Work Hours: Tuesday - Saturday, 8:00 - 16:00\n\n"
            "3. **Doctor Natalia Shevchenko**\n"
            "   - Specialization: Rehabilitation Specialist\n"
            "   - Phone: +380 63 345 6789\n"
            "   - Work Hours: Monday - Friday, 10:00 - 18:00\n\n"
            "4. **Doctor Mikhail Lysenko**\n"
            "   - Specialization: Orthopedist\n"
            "   - Phone: +380 95 456 7890\n"
            "   - Work Hours: Wednesday - Sunday, 9:00 - 17:00\n\n"
            "5. **Doctor Anna Smirnova**\n"
            "   - Specialization: Nutritionist\n"
            "   - Phone: +380 66 567 8901\n"
            "   - Work Hours: Monday - Friday, 9:00 - 16:00\n\n"
            "6. **Doctor Vasyl Koval**\n"
            "   - Specialization: Cardiologist\n"
            "   - Phone: +380 68 678 9012\n"
            "   - Work Hours: Monday - Saturday, 10:00 - 18:00\n\n"
            "7. **Doctor Daria Bondarenko**\n"
            "   - Specialization: Dermatologist\n"
            "   - Phone: +380 97 789 0123\n"
            "   - Work Hours: Tuesday - Saturday, 9:00 - 15:00\n\n"
            "8. **Doctor Oleksandr Tkachuk**\n"
            "   - Specialization: Respiratory Therapist\n"
            "   - Phone: +380 73 890 1234\n"
            "   - Work Hours: Wednesday - Sunday, 8:00 - 14:00"
        )

fnc_ctx = AssistantFnc()

@dataclass
class SessionConfig:
    openai_api_key: str
    instructions: str
    voice: openai.realtime.api_proto.Voice
    temperature: float
    max_response_output_tokens: str | int
    modalities: list[openai.realtime.api_proto.Modality]
    turn_detection: openai.realtime.ServerVadOptions

    def __post_init__(self):
        if self.modalities is None:
            self.modalities = self._modalities_from_string("text_and_audio")

    def to_dict(self):
        return {k: v for k, v in asdict(self).items() if k != "openai_api_key"}

    @staticmethod
    def _modalities_from_string(modalities: str) -> list[str]:
        modalities_map = {
            "text_and_audio": ["text", "audio"],
            "text_only": ["text"],
        }
        return modalities_map.get(modalities, ["text", "audio"])

    def __eq__(self, other: SessionConfig) -> bool:
        return self.to_dict() == other.to_dict()


def parse_session_config(data: Dict[str, Any]) -> SessionConfig:
    turn_detection = None

    if data.get("turn_detection"):
        turn_detection_json = json.loads(data.get("turn_detection"))
        turn_detection = openai.realtime.ServerVadOptions(
            threshold=turn_detection_json.get("threshold", 0.5),
            prefix_padding_ms=turn_detection_json.get("prefix_padding_ms", 200),
            silence_duration_ms=turn_detection_json.get("silence_duration_ms", 1500),
        )
    else:
        turn_detection = openai.realtime.DEFAULT_SERVER_VAD_OPTIONS

    config = SessionConfig(
        openai_api_key=data.get("openai_api_key", ""),
        instructions=data.get("instructions", ""),
        voice=data.get("voice", "alloy"),
        temperature=float(data.get("temperature", 0.8)),
        max_response_output_tokens=data.get("max_output_tokens")
        if data.get("max_output_tokens") == "inf"
        else int(data.get("max_output_tokens") or 2048),
        modalities=SessionConfig._modalities_from_string(
            data.get("modalities", "text_and_audio")
        ),
        turn_detection=turn_detection,
    )
    return config


async def entrypoint(ctx: JobContext):
    logger.info(f"connecting to room {ctx.room.name}")
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    participant = await ctx.wait_for_participant()

    run_multimodal_agent(ctx, participant)

    logger.info("agent started")


def run_multimodal_agent(ctx: JobContext, participant: rtc.Participant):
    metadata = json.loads(participant.metadata)
    config = parse_session_config(metadata)

    logger.info(f"starting MultimodalAgent with config: {config.to_dict()}")

    if not config.openai_api_key:
        raise Exception("OpenAI API Key is required")

    model = openai.realtime.RealtimeModel(
        api_key=config.openai_api_key,
        instructions=config.instructions,
        voice=config.voice,
        temperature=config.temperature,
        max_response_output_tokens=config.max_response_output_tokens,
        modalities=config.modalities,
        turn_detection=config.turn_detection,
        # model="ft:gpt-4o-mini-2024-07-18:fai-s-tudio:kvitka:ATGvsK8F",
    )
    assistant = MultimodalAgent(model=model, fnc_ctx=fnc_ctx)
    assistant.start(ctx.room)
    session = model.sessions[0]

    if config.modalities == ["text", "audio"]:
        session.conversation.item.create(
            llm.ChatMessage(
                role="user",
                content="Please begin the interaction with the user in a manner consistent with your instructions.",
            )
        )
        session.response.create()

    @ctx.room.local_participant.register_rpc_method("pg.updateConfig")
    async def update_config(
        data: rtc.rpc.RpcInvocationData,
    ):
        if data.caller_identity != participant.identity:
            return

        new_config = parse_session_config(json.loads(data.payload))
        if config != new_config:
            logger.info(
                f"config changed: {new_config.to_dict()}, participant: {participant.identity}"
            )
            session = model.sessions[0]
            session.session_update(
                instructions=new_config.instructions,
                voice=new_config.voice,
                temperature=new_config.temperature,
                max_response_output_tokens=new_config.max_response_output_tokens,
                turn_detection=new_config.turn_detection,
                modalities=new_config.modalities,
            )
            return json.dumps({"changed": True})
        else:
            return json.dumps({"changed": False})

    @session.on("response_done")
    def on_response_done(response: openai.realtime.RealtimeResponse):
        variant: Literal["warning", "destructive"]
        description: str | None = None
        title: str
        if response.status == "incomplete":
            if response.status_details and response.status_details["reason"]:
                reason = response.status_details["reason"]
                if reason == "max_output_tokens":
                    variant = "warning"
                    title = "Max output tokens reached"
                    description = "Response may be incomplete"
                elif reason == "content_filter":
                    variant = "warning"
                    title = "Content filter applied"
                    description = "Response may be incomplete"
                else:
                    variant = "warning"
                    title = "Response incomplete"
            else:
                variant = "warning"
                title = "Response incomplete"
        elif response.status == "failed":
            if response.status_details and response.status_details["error"]:
                error_code = response.status_details["error"]["code"]
                if error_code == "server_error":
                    variant = "destructive"
                    title = "Server error"
                elif error_code == "rate_limit_exceeded":
                    variant = "destructive"
                    title = "Rate limit exceeded"
                else:
                    variant = "destructive"
                    title = "Response failed"
            else:
                variant = "destructive"
                title = "Response failed"
        else:
            return

        asyncio.create_task(show_toast(title, description, variant))

    async def send_transcription(
        ctx: JobContext,
        participant: rtc.Participant,
        track_sid: str,
        segment_id: str,
        text: str,
        is_final: bool = True,
    ):
        transcription = rtc.Transcription(
            participant_identity=participant.identity,
            track_sid=track_sid,
            segments=[
                rtc.TranscriptionSegment(
                    id=segment_id,
                    text=text,
                    start_time=0,
                    end_time=0,
                    language="en",
                    final=is_final,
                )
            ],
        )
        await ctx.room.local_participant.publish_transcription(transcription)

    async def show_toast(
        title: str,
        description: str | None,
        variant: Literal["default", "success", "warning", "destructive"],
    ):
        await ctx.room.local_participant.perform_rpc(
            destination_identity=participant.identity,
            method="pg.toast",
            payload=json.dumps(
                {"title": title, "description": description, "variant": variant}
            ),
        )

    last_transcript_id = None

    # send three dots when the user starts talking. will be cleared later when a real transcription is sent.
    @session.on("input_speech_started")
    def on_input_speech_started():
        nonlocal last_transcript_id
        remote_participant = next(iter(ctx.room.remote_participants.values()), None)
        if not remote_participant:
            return

        track_sid = next(
            (
                track.sid
                for track in remote_participant.track_publications.values()
                if track.source == rtc.TrackSource.SOURCE_MICROPHONE
            ),
            None,
        )
        if last_transcript_id:
            asyncio.create_task(
                send_transcription(
                    ctx, remote_participant, track_sid, last_transcript_id, ""
                )
            )

        new_id = str(uuid.uuid4())
        last_transcript_id = new_id
        asyncio.create_task(
            send_transcription(
                ctx, remote_participant, track_sid, new_id, "…", is_final=False
            )
        )

    @session.on("input_speech_transcription_completed")
    def on_input_speech_transcription_completed(
        event: openai.realtime.InputTranscriptionCompleted,
    ):
        nonlocal last_transcript_id
        if last_transcript_id:
            remote_participant = next(iter(ctx.room.remote_participants.values()), None)
            if not remote_participant:
                return

            track_sid = next(
                (
                    track.sid
                    for track in remote_participant.track_publications.values()
                    if track.source == rtc.TrackSource.SOURCE_MICROPHONE
                ),
                None,
            )
            asyncio.create_task(
                send_transcription(
                    ctx, remote_participant, track_sid, last_transcript_id, ""
                )
            )
            last_transcript_id = None

    @session.on("input_speech_transcription_failed")
    def on_input_speech_transcription_failed(
        event: openai.realtime.InputTranscriptionFailed,
    ):
        nonlocal last_transcript_id
        if last_transcript_id:
            remote_participant = next(iter(ctx.room.remote_participants.values()), None)
            if not remote_participant:
                return

            track_sid = next(
                (
                    track.sid
                    for track in remote_participant.track_publications.values()
                    if track.source == rtc.TrackSource.SOURCE_MICROPHONE
                ),
                None,
            )

            error_message = "⚠️ Transcription failed"
            asyncio.create_task(
                send_transcription(
                    ctx,
                    remote_participant,
                    track_sid,
                    last_transcript_id,
                    error_message,
                )
            )
            last_transcript_id = None


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, worker_type=WorkerType.ROOM))
