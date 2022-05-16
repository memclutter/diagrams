from diagrams import Cluster, Diagram
from diagrams.k8s.group import Namespace
from diagrams.k8s.network import Ingress, Service
from diagrams.k8s.compute import Deployment, Pod
from diagrams.onprem.database import Postgresql
from diagrams.onprem.queue import Rabbitmq
from diagrams.onprem.logging import Fluentbit
from diagrams.elastic.elasticsearch import Elasticsearch, Kibana


with Diagram("K8S Logging", filename="k8s_logging"):

    with Cluster("K8S Cluster"):
        ingress = Ingress("ingress")
        with Cluster("namespace=app"):

            with Cluster("deployment=backend"):
                backend_service = Service("backend")
                backend_pod = Pod("backend")
            
            with Cluster("deployment=frontend"):
                frontend_service = Service("frontend")
                frontend_pod = Pod("frontend")

        with Cluster("namespace=logging"):
            agent = Fluentbit("agent")
            es = Elasticsearch("elastic")
            kibana = Kibana("kibana")
            kibana_serice = Service("kibana")

            agent >> es >> kibana
            kibana_serice >> kibana

        with Cluster("namespace=db"):
            db = Postgresql("db")
            
        with Cluster("namespace=eventbus"):
            eventbus = Rabbitmq("eventbus")

        ingress >> backend_service >> backend_pod
        ingress >> frontend_service >> frontend_pod
        ingress >> kibana_serice

        backend_pod >> db
        backend_pod << db
        backend_pod >> eventbus
        backend_pod << eventbus

        backend_pod >> agent
        frontend_pod >> agent

        db >> agent
        eventbus >> agent
