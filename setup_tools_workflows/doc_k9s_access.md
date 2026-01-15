# **k9s-access.sh Documentation**

## **Overview**
`k9s-access.sh` is a Bash script that automates the process of:
1. **Setting up a secure SSH tunnel** to a remote Kubernetes cluster
2. **Copying and configuring the kubeconfig** for local access
3. **Auto-launching k9s** (terminal UI for Kubernetes)

This script is ideal for quickly accessing remote Kubernetes clusters without manual SSH tunneling and kubeconfig management.

---

## **Prerequisites**
- **Bash** (Linux/macOS)
- **SSH** access to the remote host (`MONIT-DSSP` by default)
- **k9s** installed (Kubernetes CLI dashboard)
- **scp** (for copying kubeconfig)
- **sed** (for modifying kubeconfig)

---

## **Installation**
1. **Save the script** as `k9s-access.sh`:
   ```bash
   curl -o k9s-access.sh https://gist.githubusercontent.com/your-username/your-gist-id/raw/k9s-access.sh
   ```
2. **Make it executable**:
   ```bash
   chmod +x k9s-access.sh
   ```
3. **Move to a PATH directory** (optional):
   ```bash
   sudo mv k9s-access.sh /usr/local/bin/
   ```

---

## **Usage**
### **1. Start the Tunnel & Launch k9s**
```bash
./k9s-access.sh
```
**What happens?**
- Copies the remote kubeconfig (`/etc/rancher/k3s/k3s.yaml`) to `~/.kube/config`
- Modifies the kubeconfig to use `localhost:6443`
- Establishes an SSH tunnel in the background
- Automatically opens **k9s**

---

### **2. Stop the Tunnel**
```bash
./k9s-access.sh --stop
```
**What happens?**
- Kills the background SSH tunnel
- Cleans up the PID file

---

### **3. Custom Host/Port (Optional)**
Modify the script variables at the top:
```bash
REMOTE_HOST="your-remote-host"  # Change default host
SSH_PORT=2222                  # Custom SSH port (default: 22)
TUNNEL_PORT=6444               # Custom tunnel port (default: 6443)
```

---

## **Troubleshooting**
### **Common Issues**
| Issue | Solution |
|-------|----------|
| **"Failed to copy kubeconfig"** | Ensure SSH access to `REMOTE_HOST` and correct `REMOTE_KUBECONFIG` path |
| **"Port 6443 already in use"** | Change `TUNNEL_PORT` or kill existing processes (`lsof -i :6443`) |
| **"k9s not found"** | Install k9s (`brew install k9s` / `curl -sS https://webinstall.dev/k9s | bash`) |

### **Logs**
Check `/tmp/k8s-tunnel.log` for SSH errors:
```bash
cat /tmp/k8s-tunnel.log
```

---

## **Example Workflow**
```bash
# Start tunnel + k9s
$ ./k9s-access.sh
[✓] Tunnel is running in background (PID: 12345)
[✓] Launching k9s...

# After work, stop the tunnel
$ ./k9s-access.sh --stop
[✓] Cleaning up...
[✓] Stopped tunnel (PID: 12345)
```

---

## **Notes**
- **No `kubectl` required** – Works directly with `k9s`
- **Persistent tunnel** – Runs in the background until stopped
- **Security** – Uses SSH encryption; no Kubernetes credentials stored

---

🚀 **Enjoy seamless Kubernetes access with `k9s-access.sh`!**