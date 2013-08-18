# Comments Aware Enter for Sublime Text 2/3

Hitting `Enter` in line comments will insert a proper indented comment marker for you.

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


## Bugs

- don't work if cursor is at very end of a file (A bug in Sublime Text 2)

## TODO

- switch from language to line-comment scope detection
