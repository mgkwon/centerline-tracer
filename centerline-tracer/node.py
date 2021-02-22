#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rospy

if __name__ == '__main__':
    node_name = 'centerline-tracer'
    rospy.init_node(node_name, log_level=rospy.INFO)

    rospy.spin()
