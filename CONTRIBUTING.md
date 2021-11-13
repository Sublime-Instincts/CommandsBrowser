Contributions in any form is most welcome ! Some of the areas that could use improvements are

1. Improve existing commands documentation (command descriptions, arguments descriptions etc.)
2. Add documentation to existing commands that don't have one.
3. Add new commands that have been missed from this list.
4. Improved ways of presenting the information to the user.

Here are the general steps to setup a work environment and to get started

1. Fork the repository and `git clone` your fork to the `Packages/` directory.
2. Refer to the `.editorconfig` file and setup the specific settings. I usually just create a [Project]() for each package and set up project specific settings for them

```json
{
    "folders":
    [
        {
            "path": "C:\\Users\\DELL\\AppData\\Roaming\\Sublime Text\\Packages\\CommandsBrowser"
        },
        {
            "path": "C:\\Users\\DELL\\AppData\\Roaming\\Sublime Text\\Packages\\CommandsBrowser33"
        }
    ],
    "settings": {
        "tab_size": 4,
        "default_encoding": "UTF-8",
        "default_line_ending": "unix",
        "translate_tabs_to_spaces": true,
        "ensure_newline_at_eof_on_save": true,
        "trim_trailing_white_space_on_save": "all",
    },
}
```

3. Create a new branch off of the `master` and make your changes there.
4. Push the branch to your remote fork and then create a PR to `master`.
5. Wait for your PR to be reviewed. It may take some time to review so don't be disheartened if it's not done immediately.
6. The PR get's merged to `master` and you have made an amazing contribution to keep the open source spirit alive ! You are awesome 😊
