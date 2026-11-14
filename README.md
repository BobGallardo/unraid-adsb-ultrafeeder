# ADS-B Ultrafeeder for Unraid

An Unraid Docker template for [SDR-Enthusiasts ADS-B Ultrafeeder](https://github.com/sdr-enthusiasts/docker-adsb-ultrafeeder). Use a compatible ADS-B receiver to track nearby aircraft on a local map, monitor receiver performance, and optionally share data with flight-tracking services.

This community-maintained repository supplies the **Unraid installation template**. The Ultrafeeder application and Docker image are developed separately by SDR-Enthusiasts.

> **Project status:** This template is in pre-release testing and is **not yet listed in Unraid Community Apps**. Its configuration has not yet been verified on physical Unraid hardware. Follow the manual installation instructions below until a Community Apps release is available.

## Features

- **Live aircraft map:** [tar1090](https://github.com/wiedehopf/tar1090) displays aircraft detected by your receiver.
- **Receiver statistics:** graphs1090 provides reception and range history.
- **RTL-SDR support:** Connect a compatible USB SDR and antenna to your Unraid server.
- **Beast data output:** Share locally decoded aircraft data with compatible feeder containers on TCP port `30005`.
- **Optional feeding and MLAT:** Configure external services if you choose; the template does **not** enable any external data-sharing destination by default.
- **Unraid Docker UI:** Configure the receiver, antenna position, networking, and optional settings without writing a Docker Compose file.

## Requirements

- An Unraid server with Docker enabled.
- A compatible ADS-B receiver (such as an RTL-SDR) and antenna, or another supported input configured according to the [upstream documentation](https://github.com/sdr-enthusiasts/docker-adsb-ultrafeeder).
- The antenna's **latitude, longitude, and altitude above mean sea level**. Include units for altitude, such as `125m` or `410ft`.
- **USB ADS-B receiver:** If you're using an RTL-SDR connected to your Unraid server, the Docker container needs permission to access it. The template includes settings for USB device access.

Only one decoder should control a given USB receiver at a time. Stop older containers such as `adsb-main` before starting Ultrafeeder with the same receiver.

## Installation

### Manual installation (current pre-release)

1. Download [`templates/adsb-ultrafeeder.xml`](templates/adsb-ultrafeeder.xml) from this repository.
2. Copy it to your Unraid flash drive as `/boot/config/plugins/dockerMan/templates-user/my-adsb-ultrafeeder.xml`.
3. In the Unraid web interface, open **Docker → Add Container** and choose the **ADS-B Ultrafeeder** template. Refresh the Docker page if the new template is not immediately listed.
4. Enter your antenna position, altitude (with units), and timezone. Review the receiver and USB settings.
5. Choose your Docker network. The default template uses **bridge**; a custom VLAN or network with a dedicated IP is also possible.
6. Apply the template, start the container, and open its WebUI.

**When this template is published to Community Apps**, installation will be available through Unraid's **Apps** tab. Until then, do not expect it to appear in Community Apps search.

### Important settings

| Unraid setting | What to enter |
| --- | --- |
| **Antenna Latitude** (`READSB_LAT`) | Decimal latitude of your receiving antenna |
| **Antenna Longitude** (`READSB_LON`) | Decimal longitude of your receiving antenna |
| **Antenna Altitude** (`READSB_ALT`) | Altitude above mean sea level, **including units** (for example `125m`) |
| **Timezone** (`TZ`) | IANA timezone such as `America/Los_Angeles` |
| **SDR Device Type** (`READSB_DEVICE_TYPE`) | Leave as `rtlsdr` for a compatible RTL-SDR receiver |
| **RTL-SDR Gain** (`READSB_GAIN`) | Start with the template's `auto` setting; tune later if needed |
| **Enable Bias Tee** (`READSB_ENABLE_BIASTEE`) | Enable only if your SDR and amplifier require bias-tee power |
| **Additional Feed Configuration** (`ULTRAFEEDER_CONFIG`) | Leave blank unless intentionally configuring remote feeds or MLAT |

The template mounts `/dev/bus/usb` and includes a USB device cgroup rule to accommodate USB device reconnections. Check these settings if the receiver is not detected. The mount exposes host USB devices to the container; understand that access before enabling it.

Other settings are available through Unraid's **Advanced View**. See the [Ultrafeeder documentation](https://github.com/sdr-enthusiasts/docker-adsb-ultrafeeder) for detailed receiver and feeding options.

## Open the aircraft map

The address depends on the Docker network selected during installation:

| Network mode | Map URL | Beast data output |
| --- | --- | --- |
| **Bridge** (template default) | `http://UNRAID-IP:8080/` | `UNRAID-IP:30005` |
| **Custom network with its own IP** | `http://CONTAINER-IP/` (port `80`) | `CONTAINER-IP:30005` |

Replace `UNRAID-IP` or `CONTAINER-IP` with the address assigned in your own installation. The template's default browser port for bridge mode is `8080`; Ultrafeeder listens on port `80` **inside** the container.

For receiver charts, open `/graphs1090` on the same web address. If you do not see aircraft immediately, check the container logs and receiver/antenna configuration before assuming the map is broken.

## Optional data sharing

Ultrafeeder can supply decoded data to other local containers and, when configured, external flight-tracking networks. **This template does not configure outbound feeding or MLAT destinations by default.**

If you already use separate flight-tracking feeder containers, review their configured Beast source and update it to the new Ultrafeeder host and TCP port `30005` as needed. For Ultrafeeder-managed feeds, use the upstream [`ULTRAFEEDER_CONFIG` documentation](https://github.com/sdr-enthusiasts/docker-adsb-ultrafeeder) and explicitly configure only the destinations you intend to use.

## Migrating from adsb-main

Follow the [migration guide](docs/migration-from-adsb-main.md) to transfer station settings and maintain compatibility with existing feeder containers. Keep a copy of your previous Unraid template until reception and downstream feeds have been verified.

## Troubleshooting

| Problem | What to check |
| --- | --- |
| **No aircraft appear** | Confirm the receiver is detected in the container logs, the antenna is connected, and the latitude/longitude are correct |
| **USB receiver unavailable** | Stop other SDR decoder containers; review the USB bus mount and device cgroup rule |
| **WebUI does not open** | Confirm the container is running and use the correct address/port for bridge versus custom-IP networking |
| **Graphs are missing** | Check `/graphs1090` and the persistent graphs1090 data mount |
| **Existing feeder containers stop receiving data** | Update their Beast source hostname/IP and verify TCP port `30005` is reachable |
| **Container fails to start** | Review the Unraid Docker container logs and verify required position and receiver settings |

For issues with the **Ultrafeeder application**, consult the [upstream project](https://github.com/sdr-enthusiasts/docker-adsb-ultrafeeder). For template-specific issues, use this template repository's issue tracker once its public repository URL is established.

## Security and privacy

- Your antenna coordinates may reveal the location of your receiver. Do not publish personal station settings or logs containing sensitive information without reviewing them.
- The template exposes a local web interface; it does not configure a public reverse proxy or internet-facing service. Actual reachability depends on your network and firewall configuration.
- Sharing data with external tracking services is optional and must be configured explicitly.
- USB access is broader than a single fixed device path. Use images you trust and keep them updated.

## Acknowledgments and contributions

Ultrafeeder is developed by [SDR-Enthusiasts](https://github.com/sdr-enthusiasts/docker-adsb-ultrafeeder). This Unraid template is an independent community project and is not an official SDR-Enthusiasts or Unraid release.

Bug reports and improvements to the **Unraid template** are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for contributor instructions and [CHANGELOG.md](CHANGELOG.md) for changes.
