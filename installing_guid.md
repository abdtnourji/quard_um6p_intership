Guid to set-up the intership working space in ubuntu 22.04,

# ROS 2 base environment

source /opt/ros/humble/setup.bash

# Project root

export IntershipUm6p_ROOT="$HOME/quard_um6p_intership"

# Custom Gazebo models.

export GZ_SIM_RESOURCE_PATH="$HOME/.gz/models${GZ_SIM_RESOURCE_PATH:+:$GZ_SIM_RESOURCE_PATH}"
BASHRC

Because your scripts 00, 01 and 02 have already run, do not restart from zero. Before continuing, verify what branches were downloaded:

cd ~/quard_um6p_intership

source config/project.env

git -C "${PX4_DIR}" branch --show-current
git -C "${ROS2_WS}/src/px4_msgs" branch --show-current
git -C "${DDS_AGENT_DIR}" branch --show-current

Ubuntu: 22.04
ROS 2: Humble
PX4: release/1.15
px4_msgs: release/1.15
Python: system Python 3.10
Core drone: gz_x500
Camera drone: gz_x500_depth, used later
Perception: CPU by default, CUDA optional

token
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

L'erreur **HTTP 401** survient parce que GitHub n'accepte plus les mots de passe classiques pour authentifier les opérations Git via le terminal (cette règle est en place depuis août 2021).

Pour cloner un dépôt qui nécessite une authentification, vous devez utiliser un **Personal Access Token (PAT)** à la place de votre mot de passe.

Voici comment résoudre ce problème en quelques minutes :

### 1. Générer un Token sur GitHub

1. Connectez-vous à votre compte sur GitHub via un navigateur web.
2. Cliquez sur votre photo de profil en haut à droite, puis allez dans **Settings**.
3. Dans le menu de gauche, descendez tout en bas et cliquez sur **Developer settings**.
4. Cliquez sur **Personal access tokens** > **Tokens (classic)**.
5. Cliquez sur le bouton **Generate new token (classic)**.
6. Donnez-lui un nom (ex: `PX4_Clone`), choisissez une date d'expiration, et **cochez la case "repo"** (Full control of private repositories).
7. Cliquez sur **Generate token** tout en bas.
8. **Copiez le token généré** (il commence généralement par `ghp_...`). _Attention : il ne s'affichera qu'une seule fois._

### 2. Relancer le script

Relancez votre commande dans le terminal :

```bash
./scripts/02_download_sources.sh

```

- **Username :** Entrez votre nom d'utilisateur habituel (`tnourjiabd`).
- **Password :** Collez le **Token (PAT)** que vous venez de copier (au lieu de votre mot de passe classique).

> **Note importante :** Le dépôt officiel de PX4 (`PX4/PX4-Autopilot`) est public. Si Git vous demande un mot de passe, c'est probablement parce que le script essaie de cloner votre propre _fork_ privé de PX4, ou parce que le lien HTTPS configuré dans le script `02_download_sources.sh` force l'authentification. L'utilisation du Token résoudra le blocage.

The error message `fatal: expected flush after ref listing` is the real culprit here.

This specific error happens when Git's network connection is abruptly dropped by a firewall, a proxy (common on university or enterprise networks), or a bug in Git's HTTP/2 implementation. Because the connection drops, Git gets confused, assumes it needs authentication, and asks for a password (which then fails because we disabled prompts).

Here is the most reliable way to fix this specific network error:

### 1. Force Git to use HTTP/1.1

Downgrading Git's HTTP protocol from HTTP/2 to HTTP/1.1 bypasses the network instability causing the "flush" error. Run this in your terminal:

```bash
git config --global http.version HTTP/1.1

```

### 2. Wipe the Corrupted Build Cache

Because the clone failed midway, CMake has left a broken folder behind. You must delete the build folder again or CMake will just instantly fail on the same step.

```bash
cd ~/quard_um6p_intership/dependencies/PX4-Autopilot
rm -rf build/px4_sitl_default

```

### 3. Rebuild

Now try compiling again. The `GIT_TERMINAL_PROMPT=0` rule you set earlier is still active, which is good.

```bash
make px4_sitl

```

---

### If it still fails after doing this:

If you are still getting blocked, your network is completely rejecting Git HTTPS traffic. You will need to tell Git to use SSH instead of HTTPS for all GitHub clones.

_Note: You must have an SSH key added to your GitHub account for this to work._

```bash
git config --global url."git@github.com:".insteadOf "https://github.com/"
rm -rf build/px4_sitl_default
make px4_sitl

```
