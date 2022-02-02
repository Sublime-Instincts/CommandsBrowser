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

## [1.1.0] - 2021-11-22
### Changed
- The command palette entries, quick panel placeholders, all use full forms for ST & SM to avoid any ambiguity (#5).

### Added
- Improved documentation for `cancel_edit_commit_message`, `navigate_back`, `navigate_forward`, `navigate_to_tag`, `open_in_editor`, `open_dir_in_sublime_text`, `show_command_palette`, `save_commit_message`, `commit`, `create_branch`, `create_tag`, `clean_working_dir`, `checkout_local_branch`, `delete_branch`, `delete_tag`, `discard_hunk`, `prompt_open_repository`, `rename_branch`, `reset` and `set_word_wrap`

## [1.2.0] - 2021-11-23

### Added
- A new setting `filter_plugin_commands_on_package` to filter plugin commands based on the package.
- Improved documentation for `select_lines`, `set_build_system`, `set_file_type`, `set_line_ending`, `show_overlay`,
`show_panel`, `single_selection`, `slurp_find_string`, `slurp_replace_string`,
`switch_file`, `discard_all_modified`, `git_config`, `navigate_to_commit_message`, `navigate_to_context_commit`
`navigate_to_commit`, `navigate_to_branch`, `navigate_to_child`, `navigate_to_parent`,
`open_in_editor`, `push_tag`, `quick_open_repository`, `stage_all_untracked`, `stage_all_unmerged` and `show_command_palette`.

## [1.2.1] - 2021-11-23

### Fixed
- Fixed a situation where installing the package for the first time causes the `py33` file to be not detected by `sublime.find_resources` & settings returns `None`, thus forcing the user to restart inorder to let changes pick up
properly (#4)

## [1.3.0] - 2021-11-24

### Fixed
- Fixed a situation where `"all"` was considered an invalid option for `filter_plugin_commands_on_package` (But it continued to work because the default fallback was `"all"`).
- Removed the trailing `, ` from command signature when <kbd>ctrl</kbd> (or the configured modifier key) is used to copy command signature to clipboard.

### Added
- Added command palette and main menu entries for viewing documentation.
- Added command palette entry for opening key bindings.

## [1.4.0] - 2021-02-02

### Fixed
- Use color based kind ids instead of semantic kind ids for command type icons so that the command icons looks similar on theme using image textures (#6).

### Added
- Document `patter` & `replace_pattern` arguments for `show_panel` & `group` for `open_file` commands.
- Document `clear_recent_missing`, `open_repository` commands on Sublime Merge.
- Improved documentation for following SM commands: `close_by_index`, `close_deleted_files`, `close_others_by_index`, `close_selected`, `close_to_right_by_index`, `close_unmodified`, `close_unmodified_to_right_by_index`, `delete_tag_on_remote`, `gitflow_finish_feature`, `gitflow_finish_release`, `gitflow_start_feature`, `gitflow_start_bugfix`, `init_gitflow`, `push`.
- Improved documentation for the following ST commands: `move_to_neighboring_group`
- Added command palette entry for opening the wiki documentation.
