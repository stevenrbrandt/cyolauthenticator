# CYOLAuthenticator: Create Your Own Login Authenticator
A Jupyterhub authenticator that allows users to pick a name and password if they know a code.

This branch is a heavily modified version that runs in the Google
Cloud Platform environment.

The front-end web service runs on a Google Compute Engine VM in a
docker container (`dstndstn/cyol`), described in the `hub/`
directory.  This includes a persistent disk mounted in `/nfs`, which
holds user home directories as well as persistent state for the
service. It also runs an LDAP server, and exports the home directories
via NFS.

The notebook servers are started on Kubernetes pods, which run the
`dstndstn/cyol-singleuser` container (in the `singleuser/` directory).
The notebooks are run as the logged-in user, and the home directory is
mounted over NFS.

## Old instructions

To enable users to create a login, place a code word in
`/usr/enable_mkuser`. If the users provide this code word when
attempting to create a login, they will succeed.

To disable creation of logins, remove `/usr/enable_mkuser`.

Note that you will also need a custom `login.html` page. See the docker
directory for how to do this.

## Google Cloud Platform Setup instructions

- in Google Kubernetes Engine, create a cluster to run your notebook
  servers.

- in Google Compute Engine, create a persistent volume called `nfs-home`,
  initiatize it with a filesystem (probably `ext4`), and add:
  - `sys/svc.json` containing a JSON-format service account credential
    for Kubernetes
  - `home/` directory
  - Optionally, `sys/ldap/data.mdb` containing the LDAP database

- Run:
```
kubectl apply -f config/nfs-pv.yaml
kubectl apply -f config/nfs-pvc.yaml
```

- change the firewall rules to allow traffic between GCE and your GKE cluster:
```
# PER https://cloud.google.com/kubernetes-engine/docs/troubleshooting#autofirewall
$ gcloud container clusters describe your-first-cluster-1 --format=get"(network)" --zone us-central1-a
default
$ gcloud container clusters describe your-first-cluster-1 --format=get"(clusterIpv4Cidr)" --zone us-central1-a
10.4.0.0/14
$ gcloud compute firewall-rules create "your-first-cluster-1-to-all-vms-on-network" --network="default" --source-ranges="10.4.0.0/14" --allow=tcp,udp,icmp,esp,ah,sctp
Creating firewall...
Created [https://www.googleapis.com/compute/v1/projects/research-technologies-testbed/global/firewalls/your-first-cluster-1-to-all-vms-on-network].
NAME                                        NETWORK  DIRECTION  PRIORITY  ALLOW                     DENY  DISABLED
your-first-cluster-1-to-all-vms-on-network  default  INGRESS    1000      tcp,udp,icmp,esp,ah,sctp        False
```

- start the `hub` VM with a command such as (replacing with relevant names for your project):
```
gcloud beta compute --project=research-technologies-testbed instances create-with-container hub \
 --zone=us-central1-a --machine-type=n1-standard-1 --subnet=default --network-tier=PREMIUM \
 --metadata=google-logging-enabled=true --maintenance-policy=MIGRATE \
 --service-account=310980440256-compute@developer.gserviceaccount.com \
 --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append \
 --tags=hub,http-server --image=cos-stable-77-12371-114-0 --image-project=cos-cloud --boot-disk-size=10GB \
 --boot-disk-type=pd-standard --boot-disk-device-name=hub --disk=name=nfs-home,device-name=nfs-home,mode=rw,boot=no \
 --container-image=dstndstn/cyol --container-restart-policy=always --container-privileged \
 --container-mount-disk=mount-path=/nfs,name=nfs-home,mode=rw --labels=container-vm=cos-stable-77-12371-114-0

 --container-image=gcr.io/research-technologies-testbed/cyol
```

- The GCP Project name "research-technologies-testbed" is baked into
  the `dstndstn/cyol` container image, so if you want to change that
  name, you will need to rebuild the image, and change the container
  name in the above VM-creation command line.  See also the `hub/run.sh`
  script.

