# SPDX-FileCopyrightText: 2023-present Matt Jadud <matthew.jadud@gsa.gov>
#
# SPDX-License-Identifier: MIT
import sys

if __name__ == "__main__":
    from wbc_cli.cli import wbc_cli

    sys.exit(wbc_cli())
