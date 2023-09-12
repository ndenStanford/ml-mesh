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

## Benefits of using Dask in NLP

The Python Global Interpreter Lock (GIL) is what typically prevents "pure Python" code (as opposed to Python code that calls into native extensions like NumPy or Cython functions) from running in parallel across multiple threads. In a single Python process, only one thread can execute Python bytecode at a time because of the GIL. This is why it's generally recommended to use multiple processes for CPU-bound "pure Python" code: each process runs in its own interpreter with its own GIL, allowing for true parallelism.

### Dask has a few different scheduling options to tackle parallel execution:

- Threaded Scheduler: Useful for I/O-bound or GIL-released tasks like those involving NumPy, pandas, or similar libraries that release the GIL when they do heavy computations.

- Multiprocessing Scheduler: Useful for CPU-bound tasks that are written in pure Python and don't release the GIL. This scheduler runs each task in a separate process, thus bypassing the GIL.

- Distributed Scheduler: A more general-purpose scheduler that can run tasks on distributed systems. It's more flexible and can use both threads and processes, but it involves more setup. This is what we are using via Dask Kubernetes Operator.

### Can Dask use threads in processes?

The short answer is that within a single Dask worker, you can choose either threads or processes but not both at the same time for parallel execution. Each Dask worker is a separate Python process and can use multiple threads for executing tasks, but this is still subject to the limitations of the GIL for pure Python code.

However, in a Dask distributed setup, you can have multiple workers, each running in its own process. Each of these workers can, in turn, use multiple threads (4 by default in our setup) to execute tasks that are not limited by the GIL (like NumPy operations). This way, you effectively have both multiprocessing and multithreading, but at different levels of the computation (inter-worker vs. intra-worker).

This setup allows you to combine the advantages of both worlds: multiprocessing for tasks that are GIL-bound and multithreading for tasks that can release the GIL.

## Documentation on Dask

- [`dask.org`](https://www.dask.org/)
- [`Dask Documentation`](https://docs.dask.org/en/stable/)
- [`Dask Kubernetes Documentation`](https://kubernetes.dask.org/en/latest/)
