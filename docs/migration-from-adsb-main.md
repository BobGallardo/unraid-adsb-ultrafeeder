# Migrating from `adsb-main` / `mikenye/readsb-protobuf`

This guide concerns the RTL-SDR and ADS-B decoder only; reverse proxy/TLS is outside scope.

## Before you begin

1. Record your existing station settings **locally**: latitude, longitude, timezone, tuner serial, and antenna altitude above sea level. Do not commit private coordinates to Git.
2. Inventory separate feeder containers and record their Beast host and port.
3. Save a backup of the existing Unraid `adsb-main` template from `/boot/config/plugins/dockerMan/templates-user/` and any data you need.
4. Stop the original decoder before starting Ultrafeeder. Two containers cannot reliably use the same RTL-SDR USB device simultaneously.

## Settings mapping

| Old setting | New setting | Notes |
| --- | --- | --- |
| Image `mikenye/readsb-protobuf` | `ghcr.io/sdr-enthusiasts/docker-adsb-ultrafeeder:latest` | Different image, not drop-in |
| `READSB_LAT` | `READSB_LAT` | Re-enter locally |
| `READSB_LON` | `READSB_LON` | Re-enter locally |
| (not in old XML) | `READSB_ALT` | **Required**; include `m` or `ft` |
| `TZ` | `TZ` | Use valid IANA name |
| `READSB_DEVICE_TYPE=rtlsdr` | same | Requires USB access |
| `READSB_GAIN=autogain` | `READSB_GAIN=auto` | New recommended built-in autogain |
| `READSB_FIX` | `READSB_ENABLE_BIASTEE` | Only enable if supported/needed |
| Web container port `8080` | `80` | `8080:80` on bridge, `:80` with own LAN IP |
| Beast output port `30005` | `30005` | Preserve feeder connections, update hostname if needed |

## USB access

The template mounts `/dev/bus/usb` and supplies `--device-cgroup-rule='c 189:* rwm'`. It gives the container broad access to USB devices visible on the bus; understand this trust boundary and keep the image maintained. The upstream project recommends this approach for hot-plug recovery.

## Networking

The public template defaults to Docker bridge networking. On Unraid, select a custom network if you want a dedicated IP address, and set the IP there. Docker port mappings do not work in the usual way on custom macvlan/ipvlan networks; services normally use the container's own address and internal listening ports. Do not paste the station's VLAN IP into the public XML.

## Migration verification

- Check `docker logs adsb-ultrafeeder` for receiver discovery and position decoding.
- Open the local tar1090 map and `/graphs1090`.
- Verify your prior feeder clients receive Beast data on TCP 30005.
- Confirm that no unrequested remote feeds or MLAT sessions have been enabled.
- Keep the old Unraid template for rollback until the receiver and feeder clients work.
