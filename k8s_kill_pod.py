from kubernetes import client, config
import random
import logging
import constants
import time
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

# for i in ret.items:
#     logging.info("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

def count_pods():
    config.load_kube_config()
    v1 = client.CoreV1Api()
    ret = v1.list_pod_for_all_namespaces(watch=False)
    logging.info("Connected to Kubernetes host: %s", v1.api_client.configuration.host)
    POD_COUNT = len(ret.items)
    logging.info("Number of pods: %s", POD_COUNT)

    return(POD_COUNT)

def list_pods():
    if constants.OFFLINE_MODE == True:
        return([0],[0])
    else:
        try:
            config.load_kube_config()
            v1 = client.CoreV1Api()
            ret = v1.list_pod_for_all_namespaces(watch=False)
            logging.info("Updating pod list from: %s", v1.api_client.configuration.host)
            POD_COUNT = len(ret.items)
            logging.info("Number of pods: %s", POD_COUNT)

            # Select random pod
            # print(ret.items[0].metadata.namespace)
            random.shuffle(ret.items)
            while ret.items[0].metadata.namespace in constants.EXCLUDES_LIST:
                logging.info("Pod in excluded namespace, shuffling")
                random.shuffle(ret.items)
            POD_TO_KILL = ret.items[0].metadata.name
            POD_NAMESPACE = ret.items[0].metadata.namespace
            return([POD_TO_KILL, POD_NAMESPACE])
        except Exception as e:
            logging.error("Unable to list pods: %s", (e))
            return([0],[0])


def delete_pod(name, namespace):
    # Configs can be set in Configuration class directly or using helper utility
    if constants.OFFLINE_MODE == True:
        logging.info("Crate destroyed! Offline mode, so not actually killing any pods")
        return(" ")
    else:
        try:
            config.load_kube_config()
            v1 = client.CoreV1Api()
            # logging.info(v1.api_client.configuration.host)
            logging.info("Killing Random pod: %s from namespace: %s", name, namespace)
            
            # Delete random pod
            delete_options = client.V1DeleteOptions()
            api_response = v1.delete_namespaced_pod(
                name=name,
                namespace=namespace,
                body=delete_options)
            return(name)  #TODO: Check response for successs? 
        except:
            logging.error("Unable to delete pod")
            return("Error")
