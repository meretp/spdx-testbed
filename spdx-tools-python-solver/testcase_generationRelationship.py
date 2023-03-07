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

from spdx.model.actor import Actor, ActorType
from spdx.model.checksum import Checksum, ChecksumAlgorithm
from spdx.model.document import CreationInfo, Document
from spdx.model.file import File
from spdx.model.relationship import Relationship, RelationshipType
from spdx.writer.xml.xml_writer import write_document_to_file


@click.command()
@click.option("-target", "-t", help="Path where the generated file will be stored.")
def main(target: str):
    creation_info = CreationInfo(spdx_version="SPDX-2.3", spdx_id="SPDXRef-DOCUMENT", name="document name",
                                 data_license="CC0-1.0", document_namespace="https://some.namespace",
                                 creators=[Actor(ActorType.TOOL, "test-tool")],
                                 created=datetime(2022, 1, 1))
    file1 = File(spdx_id="SPDXRef-fileA", name="./fileA.c",
                 checksums=[Checksum(ChecksumAlgorithm.SHA1, value="d6a770ba38583ed4bb4525bd96e50461655d2758")])
    file2 = File(spdx_id="SPDXRef-fileB", name="./fileB.c",
                 checksums=[Checksum(ChecksumAlgorithm.SHA1, value="d6a770ba38583ed4bb4525bd96e50461655d2758")])

    relationships = [Relationship(spdx_element_id="SPDXRef-fileA", related_spdx_element_id="SPDXRef-DOCUMENT",
                                relationship_type=RelationshipType.DESCRIBED_BY, comment="comment on DESCRIBED_BY"),
                     Relationship(spdx_element_id="SPDXRef-fileA", relationship_type=RelationshipType.DEPENDS_ON,
                                  related_spdx_element_id="SPDXRef-fileB"),
                     Relationship(related_spdx_element_id="SPDXRef-fileB", relationship_type=RelationshipType.DESCRIBES,
                                  spdx_element_id="SPDXRef-DOCUMENT"),
                     Relationship(spdx_element_id="SPDXRef-fileB", relationship_type=RelationshipType.DEPENDENCY_OF,
                                  related_spdx_element_id="SPDXRef-fileA", comment="comment on DEPENDENCY_OF")]

    doc = Document(creation_info, files=[file1, file2], relationships=relationships)
    write_document_to_file(doc, target)


if __name__ == "__main__":
    main()
