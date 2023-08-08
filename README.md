# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/Qonfused/OCE-Build/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                            |    Stmts |     Miss |   Cover |   Missing |
|-------------------------------- | -------: | -------: | ------: | --------: |
| ocebuild/pipeline/lock.py       |      195 |      151 |     23% |45-51, 66-93, 104-132, 167, 193-229, 235-243, 260-280, 292-297, 310-311, 315-317, 346-439, 451-464 |
| ocebuild/parsers/schema.py      |      158 |      138 |     13% |32-40, 63, 87-89, 105-108, 112-133, 141-144, 156-179, 185-197, 205-234, 240-266, 276-286, 292-300, 325-385 |
| ocebuild/parsers/yaml.py        |      207 |       84 |     59% |38, 42-43, 45, 48, 52, 57, 59, 104-133, 249-250, 252, 269-280, 303-379 |
| ocebuild/pipeline/kexts.py      |       89 |       77 |     13% |21-32, 62-163, 169-185 |
| ocebuild/pipeline/config.py     |       82 |       67 |     18% |42-58, 82-130, 153-165, 177-194 |
| ocebuild/pipeline/opencore.py   |       83 |       65 |     22% |33-64, 73-78, 84-88, 109-134, 159-192 |
| ocebuild/pipeline/packages.py   |       70 |       55 |     21% |40-52, 56-58, 83-139, 143-145, 167-181 |
| ocebuild/sources/resolver.py    |      167 |       43 |     74% |115, 128, 137-141, 152, 158-159, 165, 170-176, 203-205, 222, 228, 256-261, 265, 271-292, 313-321, 338-339 |
| ocebuild/pipeline/build.py      |       54 |       40 |     26% |23-26, 43-87, 97-119 |
| ocebuild/sources/github.py      |      114 |       34 |     70% |57-74, 111-113, 135-136, 152, 154-155, 228, 230, 254-257, 282-284, 305-307 |
| ocebuild/pipeline/ssdts.py      |       97 |       32 |     67% |53, 86-101, 117-127, 155, 180-196 |
| ocebuild/filesystem/posix.py    |       45 |       30 |     33% |27-31, 48, 66-69, 89-93, 114-129 |
| ocebuild/sources/binary.py      |       53 |       28 |     47% |27, 29, 35-39, 43-45, 49-56, 68-76, 88-90 |
| ocebuild/parsers/dict.py        |       46 |       28 |     39% |22-42, 78, 90-91, 103-116 |
| ocebuild/sources/dortania.py    |       42 |       24 |     43% |34-48, 54-59, 68-74, 90, 106-110 |
| ocebuild/filesystem/cache.py    |       33 |       12 |     64% |40-47, 60-66 |
| ocebuild/parsers/types.py       |       23 |        9 |     61% |40-47, 63, 67 |
| ocebuild/versioning/semver.py   |       59 |        6 |     90% |201-204, 228-230 |
| ocebuild/sources/\_lib.py       |       29 |        3 |     90% |     59-61 |
| ocebuild/parsers/\_lib.py       |       49 |        3 |     94% | 80-82, 88 |
| ocebuild/filesystem/archives.py |       28 |        3 |     89% |     51-54 |
|                       **TOTAL** | **1865** |  **932** | **50%** |           |

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