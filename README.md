# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/Qonfused/OCE-Build/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                            |    Stmts |     Miss |   Cover |   Missing |
|-------------------------------- | -------: | -------: | ------: | --------: |
| ocebuild/pipeline/lock.py       |      196 |      151 |     23% |47-53, 68-95, 106-134, 169, 195-231, 237-245, 262-282, 294-299, 312-313, 317-319, 348-441, 453-466 |
| ocebuild/pipeline/config.py     |      177 |      151 |     15% |53-74, 98-145, 168-180, 192-209, 215-254, 265-278, 282-292, 296-323, 327-339, 358-392 |
| ocebuild/parsers/schema.py      |      158 |      138 |     13% |32-40, 63, 87-89, 105-108, 112-133, 141-144, 156-179, 185-197, 205-234, 240-266, 276-286, 292-300, 325-385 |
| ocebuild/pipeline/kexts.py      |      121 |      109 |     10% |21-32, 62-209, 215-231 |
| ocebuild/parsers/yaml.py        |      210 |       87 |     59% |38, 42-43, 45, 48, 52, 57, 59, 104-139, 255-256, 258, 275-286, 309-385 |
| ocebuild/sources/github.py      |      122 |       65 |     47% |57-74, 101-113, 135-136, 155, 157-164, 237, 239, 263-266, 287-316 |
| ocebuild/pipeline/opencore.py   |       83 |       65 |     22% |32-63, 72-77, 83-87, 108-133, 158-191 |
| ocebuild/pipeline/packages.py   |       71 |       56 |     21% |40-52, 56-58, 85-143, 147-149, 171-185 |
| ocebuild/pipeline/build.py      |       70 |       54 |     23% |24-27, 44-88, 98-120, 127-141 |
| ocebuild/sources/resolver.py    |      174 |       49 |     72% |115, 128, 137-141, 152, 158-159, 165, 170-176, 203-205, 222, 228, 234-238, 256-261, 265, 271-292, 313-321, 328, 348-349 |
| ocebuild/pipeline/ssdts.py      |      110 |       43 |     61% |53, 86-101, 117-127, 155, 161-175, 200-219 |
| ocebuild/versioning/semver.py   |       91 |       34 |     63% |78-80, 211-214, 220-241, 267-294 |
| ocebuild/parsers/dict.py        |       58 |       34 |     41% |24-44, 48-57, 107-108, 120-133 |
| ocebuild/filesystem/posix.py    |       45 |       30 |     33% |27-31, 48, 66-69, 89-93, 114-129 |
| ocebuild/sources/binary.py      |       53 |       28 |     47% |27, 29, 35-39, 43-45, 49-56, 68-76, 88-90 |
| ocebuild/sources/dortania.py    |       42 |       24 |     43% |34-48, 54-59, 68-74, 90, 106-110 |
| ocebuild/filesystem/cache.py    |       33 |       12 |     64% |40-47, 60-66 |
| ocebuild/parsers/types.py       |       23 |        9 |     61% |39-46, 62, 66 |
| ocebuild/sources/\_lib.py       |       29 |        3 |     90% |     59-61 |
| ocebuild/parsers/\_lib.py       |       49 |        3 |     94% | 80-82, 88 |
| ocebuild/filesystem/archives.py |       31 |        3 |     90% |     51-54 |
|                       **TOTAL** | **2088** | **1148** | **45%** |           |

5 files skipped due to complete coverage.


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/Qonfused/OCE-Build/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/Qonfused/OCE-Build/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Qonfused/OCE-Build/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/Qonfused/OCE-Build/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2FQonfused%2FOCE-Build%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/Qonfused/OCE-Build/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.