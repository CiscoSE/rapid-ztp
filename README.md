# Rapid ZTP

*Rapid Zero-Touch Provisioning (ZTP) - Quickly deploy Cisco IOS devices*

***This project is under early Alpha development and isn't quite ready for primetime yet.  Tread cautiously!***

---

Cisco IOS configurations are readily template-able.  All you need is a powerful and intuitive templating system (thank you [Jinja](http://jinja.pocoo.org/)!) and a flexible data store for storing the data you want merged into your templates (hello [MongoDB](https://www.mongodb.com/)).  Combining the two with Cisco's [Zero-Touch Provisioning](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/prog/configuration/166/b_166_programmability_cg/zero_touch_provisioning.html) model gives you a powerfuly simple configuration engine that generates and deploys Cisco IOS configurations on-demand.

## Show Me!

- [ ] Add app demo.

## Features

Include a succinct summary of the features/capabilities of your project.

- Upload configuration templates
- Upload flexible (schemaless) device-specific configuration data (only what your template needs)
- Request device-specific configurations
- Use Cisco Zero-Touch Provisioning to automatically configure devices as they connect to the network

## Technologies & Frameworks Used

### Cisco Products & Services:

- Cisco IOS XE [Zero-Touch Provisioning](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/prog/configuration/166/b_166_programmability_cg/zero_touch_provisioning.html)
- Service

### Tools & Frameworks:

- [Jinja2](http://jinja.pocoo.org/) - Template engine
- [MongoDB](https://www.mongodb.com/) - Template and configuration-data data store
- [Responder](https://python-responder.org/) - API backend
- [Docker](https://www.docker.com/) - Container runtime environment

## Usage

- [ ] Add basic CLI instructions.

## Installation

The Rapid ZTP backend is a containerized micro-servics app.  Clone this repository then simply run:

```bash
$ docker-compose up
```

## Authors & Maintainers

Smart people responsible for the creation and maintenance of this project:

- Chris Lunsford <chrlunsf@cisco.com>

## Credits

## License

This project is licensed to you under the terms of the [Cisco Sample
Code License](./LICENSE).
