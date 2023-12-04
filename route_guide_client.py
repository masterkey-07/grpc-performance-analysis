from __future__ import print_function

import logging
import random

import grpc
import route_guide_pb2_grpc
import route_guide_resources


def generate_route(feature_list):
    for _ in range(0, 100000):
        random_feature = feature_list[random.randint(0, len(feature_list) - 1)]
        # print("Visiting point %s" % random_feature.location)
        yield random_feature.location


def guide_record_route(stub):
    feature_list = route_guide_resources.read_route_guide_database()

    route_iterator = generate_route(feature_list)
    route_summary = stub.RecordRoute(route_iterator)
    print("Finished trip with %s points " % route_summary.point_count)
    print("Passed %s features " % route_summary.feature_count)
    print("Travelled %s meters " % route_summary.distance)
    print("It took %.2fs seconds " % route_summary.elapsed_time)


def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = route_guide_pb2_grpc.RouteGuideStub(channel)
        print("-------------- RecordRoute --------------")
        guide_record_route(stub)


if __name__ == "__main__":
    logging.basicConfig()
    run()
