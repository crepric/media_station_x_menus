# Create Menus For Media Station X.

[Mediat Station X](http://msx.benzac.de/info) is a very useful app available
for smart devices such as Smart TVs. The app is fully configurable and assumes
that the media files are stored remotely and served via an HTTP server. The
files are accessed via a series of menus defined in a `json` file served by the
same server.

This utility assumes that videos are stored in a collection of folders (max
depth is 1). Each folder is expected to contain only video files and optionally
pictures, with the same name filename + the extension (`.jpg`). If the JPG file
does not exist, the utility will attempt to use `ffmpeg` to create one. You can
disable this feature by specifying the flag: `--create_thumbnails=False`.

The program checks the content of each folder, creating menu entries for each
and items representing each file. If there is a `.jpg` file, it will be used
as a thumbnail, otherwise the default movie icon is used.

## Usage

```
bazel run :create_media_station_x_menus -- \
--movies_folder <movies_root_folder> \
--url_prefix http://<server_address> \
--output_menu_file <destination_menu>
```
