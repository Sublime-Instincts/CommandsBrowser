# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2021-11-15
### Added
- Ability to view core commands for ST & SM with documentation.
- Ability to view plugin/package commands for ST with ability to navigate to source.
- Various settings to filter based on host/command type etc.
- Key binding to auto open the documentation panel for core commands.
- Using modifier keys to copy command signature to clipboard.

## [1.0.1] - 2021-11-15
### Fixed
- Fix situation when the installed package fails to read the .json files due to using wrong logic for loading the appropriate resources.

## [1.0.2] - 2021-11-15
### Fixed
- Fix core command documentation panel scrolling to the bottom when it's opened.

## [Unreleased]
### Changed
- The command palette entries, quick panel placeholders, all use full forms for ST & SM to avoid any ambiguity (#5).

### Added
- Improved documentation for the following commands

Sublime Merge
-------------

1. `cancel_edit_commit_message`
2. `navigate_back`
3. `navigate_forward`
4. `navigate_to_tag`
5. `open_in_editor`
6. `open_dir_in_sublime_text`
7. `show_command_palette`
8. `save_commit_message`

Sublime Text
------------
