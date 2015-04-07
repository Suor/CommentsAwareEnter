# Comments Aware Enter and Join Lines for Sublime Text 2/3

Hitting `Enter` in line comments will insert a proper indented comment marker for you.
In its turn `Ctrl+J` (`Cmd+J` on OS X) joins comment lines removing comment markers
and extraneous whitespace.

This plugin is for **line comments only**, so it doesn't work with block ones.


## Thats cool, but can I use `smth + Enter` instead?

Sure, just add one of the following lines to your User Preferences:

```js
{
    ...
    "linecomments_ctrl_enter": true,
    "linecomments_alt_enter": true,
    "linecomments_shift_enter": true,
    "linecomments_super_enter": true, // Stands for Cmd on Mac OS X
    ...
}
```

If any one of this options is used then plain `Enter` won't be captured, modified shortcut will be.
