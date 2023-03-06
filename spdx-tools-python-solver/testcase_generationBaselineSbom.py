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

from spdx.model.package import Package

from spdx.model.relationship import Relationship, RelationshipType

from spdx.model.actor import Actor, ActorType

from spdx.model.checksum import Checksum, ChecksumAlgorithm

from spdx.model.document import Document, CreationInfo
from spdx.model.spdx_none import SpdxNone

from spdx.writer.xml.xml_writer import write_document_to_file


@click.command()
@click.option("-target", "-t", help="Path where the generated file will be stored.")
def main(target: str):
    creation_info = CreationInfo(spdx_version="SPDX-2.3", spdx_id="SPDXRef-DOCUMENT", name="document name",
                                 document_namespace="https://some.namespace", data_license="CC0-1.0",
                                 creators=[Actor(ActorType.TOOL, "test-tool")],
                                 created=datetime(2022, 1, 1, 0, 0))
    package = Package(spdx_id="SPDXRef-somepackage", name="package name", version="2.2.1",
                      supplier=Actor(ActorType.PERSON, "Jane Doe", "jane.doe@example.com"), files_analyzed=False,
                      checksums=[Checksum(ChecksumAlgorithm.SHA1, "d6a770ba38583ed4bb4525bd96e50461655d2758")],
                      download_location=SpdxNone())
    relationship = Relationship(spdx_element_id="SPDXRef-DOCUMENT", related_spdx_element_id="SPDXRef-somepackage",
                                relationship_type=RelationshipType.DESCRIBES)
    doc = Document(creation_info, packages=[package], relationships=[relationship])
    write_document_to_file(doc, target)


if __name__ == "__main__":
    main()
