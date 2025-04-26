# KROKED

An editor for diagrams using Kroki as backend

Edit multiple textual diagrams for your project, and render them using Kroki.

Kroki is called using its REST interface on https://kroki.io/

See https://github.com/mvanriet/kroked for more information.

# Dependencies

* wxPython - `pip install wxPython`
* requests - `pip install requests`

# TODO

* select recent file from dropdown
* create new file
* save output to file, also supporting svg and PDF files
* preview svg files (possible with wxWidgets ?)
* code cleanup
* cache files and output
* set editor font
* reload last directory
* copy diagram from html view
* support file extensions like .graphviz, .mermaid, ...
* save position of sliders
* link to websites of different kinds of diagrams

# License and Copyright

   Copyright 2025  Marc Van Riet et al.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use the source code in this repository except in compliance
   with the License.

   You may find the full text of the License in the file LICENSE in the root
   of this repository, or you may obtain a copy of the License at
       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
   