# Klipper printer config

## Steps

- Disable backup creation by commenting out `os.rename(cfgname, backup_name)`
  in `~/klipper/klippy/configfile.py`.
  [Reference](https://old.reddit.com/r/klippers/comments/1134e40/why_do_i_have_so_many_cfg_files/luqve9o/)
- Set backup script and watcher to backup the config to a git repo every time
  moonraker notifies a "printer ready" state.
- Install
  [Klack-Probe-Macros](https://github.com/Harrypulvirenti/Klack-Probe-Macros)
- Install [z_calibration](https://github.com/protoloft/klipper_z_calibration)
