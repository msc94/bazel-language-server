from typing import Optional

from lsprotocol.types import TEXT_DOCUMENT_RENAME
from lsprotocol.types import (
    CreateFile,
    CreateFileOptions,
    DeleteFile,
    DeleteFileOptions,
    OptionalVersionedTextDocumentIdentifier,
    Position,
    Range,
    RenameFile,
    RenameFileOptions,
    RenameOptions,
    RenameParams,
    ResourceOperationKind,
    TextDocumentEdit,
    TextDocumentIdentifier,
    TextEdit,
    WorkspaceEdit,
)


workspace_edit = {
    "changes": {
        "uri1": [
            TextEdit(
                range=Range(
                    start=Position(line=0, character=0),
                    end=Position(line=1, character=1),
                ),
                new_text="text1",
            ),
            TextEdit(
                range=Range(
                    start=Position(line=1, character=1),
                    end=Position(line=2, character=2),
                ),
                new_text="text2",
            ),
        ],
    },
    "document_changes": [
        TextDocumentEdit(
            text_document=OptionalVersionedTextDocumentIdentifier(
                uri="uri",
                version=3,
            ),
            edits=[
                TextEdit(
                    range=Range(
                        start=Position(line=2, character=2),
                        end=Position(line=3, character=3),
                    ),
                    new_text="text3",
                ),
            ],
        ),
        CreateFile(
            kind=ResourceOperationKind.Create.value,
            uri="create file",
            options=CreateFileOptions(
                overwrite=True,
                ignore_if_exists=True,
            ),
        ),
        RenameFile(
            kind=ResourceOperationKind.Rename.value,
            old_uri="rename old uri",
            new_uri="rename new uri",
            options=RenameFileOptions(
                overwrite=True,
                ignore_if_exists=True,
            ),
        ),
        DeleteFile(
            kind=ResourceOperationKind.Delete.value,
            uri="delete file",
            options=DeleteFileOptions(
                recursive=True,
                ignore_if_not_exists=True,
            ),
        ),
    ],
}
