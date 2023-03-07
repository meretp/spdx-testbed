# Copyright (c) 2023 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from datetime import datetime

import click
from license_expression import get_spdx_licensing
from spdx.model.actor import Actor, ActorType
from spdx.model.annotation import Annotation, AnnotationType
from spdx.model.checksum import Checksum, ChecksumAlgorithm
from spdx.model.document import CreationInfo, Document
from spdx.model.file import File
from spdx.model.relationship import Relationship, RelationshipType
from spdx.model.snippet import Snippet
from spdx.writer.xml.xml_writer import write_document_to_file


@click.command()
@click.option("-target", "-t", help="Path where the generated file will be stored.")
def main(target: str):
    creation_info = CreationInfo(spdx_version="SPDX-2.3", spdx_id="SPDXRef-DOCUMENT", name="document name",
                                 data_license="CC0-1.0", document_namespace="https://some.namespace",
                                 creators=[Actor(ActorType.TOOL, "test-tool")],
                                 created=datetime(2022, 1, 1))
    snippet = Snippet(spdx_id="SPDXRef-somesnippet", file_spdx_id="SPDXRef-somefile", byte_range=(100, 400),
                      line_range=(30, 40), license_concluded=get_spdx_licensing().parse("GPL-2.0-only"),
                      license_info_in_snippet=[get_spdx_licensing().parse("GPL-2.0-only")],
                      license_comment="snippet license comment", copyright_text="Copyright 2022 Jane Doe",
                      comment="snippet comment", name="snippet name", attribution_texts=["snippet attribution"])
    annotation = Annotation(spdx_id="SPDXRef-somesnippet", annotation_type=AnnotationType.OTHER,
                            annotation_date=datetime(2022, 1, 1), annotation_comment="Snippet level annotation",
                            annotator=Actor(ActorType.PERSON, "Snippet Annotator"))
    file = File(spdx_id="SPDXRef-somefile", name="./foo.txt",
                checksums=[Checksum(ChecksumAlgorithm.SHA1, value="d6a770ba38583ed4bb4525bd96e50461655d2758")])
    relationship = Relationship(related_spdx_element_id="SPDXRef-DOCUMENT", spdx_element_id="SPDXRef-somesnippet",
                                relationship_type=RelationshipType.DESCRIBED_BY)

    doc = Document(creation_info, files=[file], snippets=[snippet], relationships=[relationship],
                   annotations=[annotation])
    write_document_to_file(doc, target)


if __name__ == "__main__":
    main()
