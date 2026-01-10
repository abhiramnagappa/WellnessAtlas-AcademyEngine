from __future__ import annotations
from typing import List, Optional, Literal
from pydantic import BaseModel, Field, HttpUrl


# --------------------
# Shared Models
# --------------------

class Attachment(BaseModel):
    filename: str = Field(..., description="File name, e.g. workbook.pdf")
    description: Optional[str] = Field(None, description="What is this attachment?")
    path: str = Field(..., description="Relative path in repo: courses/.../attachments/*.pdf")


class ChapterMarker(BaseModel):
    timestamp: str = Field(..., description="Format: mm:ss or hh:mm:ss")
    title: str = Field(..., description="Chapter title")


# --------------------
# Lesson Layer
# --------------------

class Lesson(BaseModel):
    id: str = Field(..., description="Human readable unique ID for the lesson")
    number: str = Field(
            ..., description="Lesson order number (e.g. '01.01', '03.14')"
    )
    title: str = Field(..., description="Complete title including course + section if desired")
    
    type: Literal["video", "audio", "text"] = Field(
        ..., description="Type of the primary lesson content"
    )
    
    video_url: Optional[HttpUrl] = Field(
        None, description="Full URL to video/audio/text hosted on Vimeo, SharePoint, etc."
    )
    
    duration_seconds: Optional[int] = Field(
        None, description="Length of the lesson in seconds, optional"
    )
    
    description: Optional[str] = Field(
        None, description="Short description of the lesson"
    )
    
    attachments: List[Attachment] = Field(
        default_factory=list, description="Optional supporting materials"
    )
    
    quiz: Optional[str] = Field(
        None,
        description="Optional reference to a quiz. Use a human readable ID."
    )

    transcript_path: Optional[str] = Field(
        None,
        description="Path to transcript markdown, e.g. courses/.../transcript.md"
    )

    chapter_markers: Optional[List[ChapterMarker]] = Field(
        None, description="Optional list of chapter markers for navigation"
    )


# --------------------
# Section Layer
# --------------------

class Section(BaseModel):
    id: str = Field(
        ..., description="Human readable unique ID for the section"
    )
    number: str = Field(
            ..., description="Section order number (e.g. '1', '2')"
    )
    title: str = Field(..., description="Section title")
    lessons: List[Lesson] = Field(default_factory=list, description="Lessons")


# --------------------
# Course Layer
# --------------------

class Course(BaseModel):
    id: str = Field(..., description="Human readable unique ID for the course")
    title: str = Field(..., description="Course title")
    
    tagline: Optional[str] = Field(
        None, description="One-line value proposition for the course"
    )
    
    description: Optional[str] = Field(
        None,
        description="Course description"
    )
    
    sections: List[Section] = Field(
        default_factory=list,
        description="List of sections in order"
    )

