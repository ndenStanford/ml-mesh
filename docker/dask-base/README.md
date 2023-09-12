# Dask in Kubeflow

Leverage the scalable power of Dask for big data analytics and computation in your Kubeflow notebooks hosted on a Kubernetes environment. In this setup, each user has access to a pre-configured Dask cluster named "dask-cluster" endowed with pre-defined resource limits and a ready-to-use Dask dashboard interfaced with the scheduler in their respective namespaces.
Utilize the Dask Kubernetes Operator to manage your Dask clusters efficiently in a Kubeflow environment on a Kubernetes cluster. This README walks you through setting up and using a Dask cluster configured with your prescribed resource limits and a functional Dask dashboard in your namespace.


## Setting Up Your Dask Client in a Kubeflow Notebook

Before diving into Dask computations, initialize your Dask client with your unique AIM ID. Here is how you set it up:

```
import os
os.environ['JUPYTERHUB_USER'] = "vincent.park" <-- your AIM id

from dask.distributed import Client
from dask_kubernetes.operator import KubeCluster

cluster = KubeCluster.from_name("dask-cluster", shutdown_on_close=False)
client = Client(cluster)
client
```

## Dask Dashboard

After initializing the client, you can access the Dask dashboard through your namespace, offering a real-time graphical representation of your cluster’s activity and health status. It is an invaluable tool for monitoring and debugging.

# Dask Kubernetes Operator

Dask Kubernetes Operator is a management layer facilitating the seamless deployment and scaling of Dask clusters on a Kubernetes environment. It aids in:

- Simplified Deployment: Enabling one-step deployment of Dask clusters.
- Resource Management: Managing the computational resources effectively by adhering to the specified limits.
- Automated Scaling: Automatically scaling the Dask clusters based on the workload.


## Distributed Computing with Dask

Dask enables you to carry out distributed computations, effectively handling large data workloads by splitting them into smaller pieces processed in parallel. Dask’s integration with familiar Python APIs, like NumPy, Pandas, and Scikit-learn, allows for a smooth transition to scalable data analytics and machine learning pipelines.

### Key Features:
- Lazy Evaluation: Allows for optimized execution plans and resource usage.
- Integration with Python Scientific Stack: Leverages existing Python APIs for a smoother learning curve.
- Fault Tolerance: Ensures computational reliability even in the presence of failures.


## Documentation on Dask

- [`dask.org`](https://www.dask.org/)
- [`Dask Documentation`](https://docs.dask.org/en/stable/)
- [`Dask Kubernetes Documentation`](https://kubernetes.dask.org/en/latest/)
