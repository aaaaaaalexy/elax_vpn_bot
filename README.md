# elaxvpn

Telegram Bot + WireGuard + Yookassa

## Instalation

### 1. Install Docker

If you haven't installed Docker yet, see https://docs.docker.com/engine/install/ how you can do it. 

### 2. Clone repository

For example:

```bash
git clone https://github.com/aaaaaaalexy/elax_vpn_bot.git
```

### 3. Edit .env

#### 1. Rename .env.example to .env:

```bash
mv .env.example .env
```

#### 2. Edit .env :

For example:

```
vim .env
```

Replace the <...> fields with your data:

```
BOT_TOKEN=<...> # Telegram Bot Token

YOOKASSA_ACCOUNT_ID=<...> # Yookassa account_id
YOOKASSA_SECRET_KEY=<...> # Yookassa secret_key

PG_USER=<...> # PostgreSQl User name
PG_PASSWORD=<...> # PostgreSQl User password

WG_HOST=<...> # WireGuard Host (by default 'eth0')
```

### 4. Run elaxvpn

To run elaxvpn, simply run:

```bash
cd elax_vpn_bot
docker compose \
-f docker-compose.yml \
up --detach
```

## Updating

To update to the latest version, simply run:

```bash
cd elax_vpn_bot
docker compose down --rmi local
git fetch

```

And then run the `docker compose \ ...` command above again.