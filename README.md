# Hello World


##### Architecture Decision Records


#### What is the execution environment ?

I am considering a few solution here:

* [AWS Lambda](https://aws.amazon.com/lambda/) could run the packaged code directly or even a docker image to adhere to a more open standard
* Kubernetes, specifically [EKS](https://aws.amazon.com/eks/)


For this specific case [AWS Lambda](https://aws.amazon.com/lambda/) would make sense but there are a few specific reasons to go with [EKS](https://aws.amazon.com/eks/):

1) The tasks allows for AWS or GPC and using Kubernetes as an abstraction layer for both of them should allow multi-cloud deployment
2) With [AWS Lambda](https://aws.amazon.com/lambda/) there are limitation (execution time) and I am not sure if this is a no-go in the future
3) With Kubernetes I have more control and ability to over-engineer the tasks (not a production requirement but using something like [Chalice](https://aws.github.io/chalice/index.html) would make the task extremely boring)


#### What storage solution should I use ?

Looking at the requirements (storing a date for a username) I think a key-value data store makes the most sense as we only have on relationship.
Redis looks like a good candidate:

* It scaled well
* It is available on both cloud providers
* I can run it locally or in a review environment

The only downsized is the durability of the data.
For AWS we have [MemoryDB](https://aws.amazon.com/memorydb/) that can guaranteed durability.

For GCP the situation is a bit more complicated.
[Memorystore](https://cloud.google.com/memorystore/docs/redis/redis-overview) supports only [point in time snapshots](https://cloud.google.com/memorystore/docs/redis/redis-overview#differences_between_managed_and_open_source_redis) this will expose us to always lose a wind's of time.
So will either have to use Redis Labs as a provider for this or we host our own in GKE


There is another option I was looking it but I don't have the time to implement a PoC for it:
To use two separate products and abstract them at the code level. For example use [dynamodb](https://aws.amazon.com/dynamodb/) for AWS and [Cloud Firestore](https://firebase.google.com/docs/firestore) for GPC.
