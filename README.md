# Dota 2 Aggregation

Dota 2 player data aggregator, allows you to get a small summary of KDA and KP

# Roadmap:
- [x] mvp
- [ ] tests
- [ ] ci/cd
- [ ] Dockerfile

# Installation:
```bash
make -f Makefile install-deps
```

# How to start this stuff:
```bash
make -f Makefile run-server
```

# How to use this stuff:
For example:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"account_id": 86745912, "name": "test"}' 0.0.0.0:8080/agregate
```
