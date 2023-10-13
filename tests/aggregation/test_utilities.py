from preflibtools.instances.preflibinstance import OrdinalInstance
from preflibtools.aggregation.utilities import *

from unittest import TestCase
import pytest


@requires_preference_type("soc", "toc")
def some_function(instance):
    pass

@requires_approval
def some_approval_function(instance):
    pass

class TestTypeDecorator(TestCase):

    def test_decorator_preft_type_1(self):
        instance = OrdinalInstance()
        orders = [((0,), (1,), (2,)), ((2,), (0,), (1,))]
        instance.append_order_list(orders)

        some_function(instance)


    def test_decorator_preft_type_2(self):
        instance = OrdinalInstance()
        orders = [((0,), (1,), (2,)), ((2,), (1,))]
        instance.append_order_list(orders)

        with pytest.raises(PreferenceIncompatibleError):
            some_function(instance)


    def test_decorator_preft_type_3(self):
        instance = OrdinalInstance()
        orders = [((0,1), (2,)), ((2,), (1,))]
        instance.append_order_list(orders)

        with pytest.raises(PreferenceIncompatibleError):
            some_function(instance)


class TestApprovalDecorator(TestCase):

    def test_decorator_approval(self):
        instance = OrdinalInstance()
        orders = [((0,), (1,), (2,)), ((2,), (0,), (1,))]
        instance.append_order_list(orders)

        with pytest.raises(PreferenceIncompatibleError):
            some_approval_function(instance)
    
    def test_decorator_approval(self):
        instance = OrdinalInstance()
        orders = [((0,), (1,2)), ((2,0,), (1,))]
        instance.append_order_list(orders)

        some_approval_function(instance)