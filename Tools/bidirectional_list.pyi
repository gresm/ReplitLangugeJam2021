from typing import Optional, Sequence, TypeVar, Any, Generic, Union, Literal


class BiDirectionalListEmpty:
    pass


_StackVal = TypeVar("_StackVal", object, type, Any)
_StackIterWayTrue = Literal[True]
_StackIterWayFalse = Literal[False]
_StackIterWay = TypeVar("_StackIterWay", _StackIterWayTrue, _StackIterWayFalse)


class BiDirectionalListElement(Generic[_StackVal]):
    """
    Element in stack
    value - element value
    before - element before this element (on stack)
    after - element after this element (on stack)
    """
    
    value: _StackVal
    before: "Optional[BiDirectionalListElement[_StackVal]]"
    after: "Optional[BiDirectionalListElement[_StackVal]]"
    
    def __init__(self, value: Optional[_StackVal] = None, before: Optional["BiDirectionalListElement[_StackVal]"] = None,
                 after: Optional["BiDirectionalListElement[_StackVal]"] = None):
        """
        Initialize new BiDirectionalListElement object
        :param value: value 
        :param before: element before
        :param after: element after
        """
        ...

    def __str__(self):
        """
        Implementation of str(metacls)
        :return: string
        """
        ...

    def __repr__(self):
        """
        Implementation of repr(metacls)
        :return: string
        """
        ...
    
    def _str_a(self): ... # undocumented
    
    def _str_b(self): ... # undocumented 


class BiDirectionalList(Generic[_StackVal]):
    """
    BiDirectionalList
    first - first BiDirectionalListElement object on stack
    last - last BiDirectionalListElement object on stack
    length - length of stack
    """

    first: BiDirectionalListElement[_StackVal]
    last: BiDirectionalListElement[_StackVal]
    length: int
    
    def __init__(self, *elements: _StackVal):
        """
        Initialize new BiDirectionalList object
        :param elements: Any
        """
        ...

    def empty(self):
        """
        Removes everything from stack
        :return: None
        """
        ...

    def pop_all(self) -> _StackVal:
        """
        Removes everything from stack and return removed values
        :return: list of Any
        """
        ...

    def push_last(self, value: _StackVal):
        """
        Pushes new value on the end of the stack
        :param value: Any
        :return: None
        """
        ...

    def push_all_from_last(self, values: Sequence[_StackVal]):
        """
        Pushes all values on end of stack
        Last element form sequence will end as last element of stack
        :param values: Sequence of any
        :return: None
        """
        ...

    def pop_last(self) -> _StackVal:
        """
        Removes last value from stack and returns it
        raises IndexError("End of stack") if stack is empty
        :return: Any
        """
        ...

    def push_first(self, value: _StackVal):
        """
        Pushes new value on the start of the stack
        :param value: Any
        :return: None
        """
        ...

    def push_all_from_first(self, values: Sequence[_StackVal]):
        """
        Pushes all values on start of stack
        Last element form sequence will end as first element of stack
        :param values: Sequence of any
        :return: None
        """
        ...

    def pop_first(self) -> _StackVal:
        """
        Removes first value from stack and returns it
        raises IndexError("End of stack") if stack is empty
        :return: Any
        """
        ...

    def from_first(self) -> "BiDirectionalListValuesIter[_StackVal, _StackIterWayFalse]":
        """
        Returns BiDirectionalListValuesIter that iterate through stack values from start
        :return: BiDirectionalListValuesIter
        """
        ...

    def from_last(self) -> "BiDirectionalListValuesIter[_StackVal, _StackIterWayTrue]":
        """
        Returns BiDirectionalListValuesIter that iterate through stack values from end
        :return: BiDirectionalListValuesIter
        """
        ...

    def raw_from_first(self) -> "BiDirectionalListElementIter[_StackVal, _StackIterWayFalse]":
        """
        Returns BiDirectionalListElementIter that iterate through stack elements from start
        :return: BiDirectionalListElementIter
        """
        ...

    def raw_from_last(self) -> "BiDirectionalListElementIter[_StackVal, _StackIterWayTrue]":
        """
        Returns BiDirectionalListElementIter that iterate through stack elements from end
        :return: BiDirectionalListElementIter
        """
        ...

    def __iter__(self) -> "BiDirectionalListValuesIter[_StackVal, _StackIterWayFalse]":
        """
        Implementation of iter(metacls)
        :return: BiDirectionalListValuesIter that iterate through stack values from start
        """
        ...

    def __repr__(self) -> str:
        """
        Implementation of "repr(metacls)"
        :return: string
        """
        ...
    
    def __str__(self) -> str:
        """
        Implementation of "str(metacls)"
        :return: 
        """

    def __len__(self) -> int:
        """
        Implementation of "len(metacls)"
        :return: int
        """
        ...

    def __contains__(self, item: Union[_StackVal, Any]) -> bool:
        """
        Implementation of "item in metacls"
        :param item: value to check if stack contains it
        :return: bool
        """
        ...


class BiDirectionalListElementIter(Generic[_StackVal, _StackIterWay]):
    """
    Iterator that goes through BiDirectionalList object elements
    stack - starting point(BiDirectionalListElement)
    reverse - is reversed iteration(bool)
    current - current element(BiDirectionalListElement)
    """
    
    stack: BiDirectionalListElement[_StackVal]
    reverse: _StackIterWay
    current: BiDirectionalListElement[_StackVal]
    
    def __init__(self, stack: BiDirectionalListElement[_StackVal], reverse: _StackIterWay = _StackIterWayFalse):
        """
        Initialize new BiDirectionalListElementIter object
        :param stack: starting point for iteration(BiDirectionalListElement)
        :param reverse: reversed iteration(bool)
        """
        ...

    def __iter__(self) -> "BiDirectionalListElementIter[_StackVal, _StackIterWay]":
        """
        Implementation of iter(metacls)
        :return: metacls
        """
        return self

    def __next__(self) -> BiDirectionalListElement[_StackVal]:
        """
        Implementation of next(metacls)
        :return: current element(BiDirectionalListElement)
        """
        ...


class BiDirectionalListValuesIter(Generic[_StackVal, _StackIterWay]):
    """
    Iterator that goes through BiDirectionalList object values
    _iter - real iterator(BiDirectionalListElementIter)
    """
    
    _iter: BiDirectionalListElementIter[_StackVal, _StackIterWay]
    
    def __init__(self, stack: BiDirectionalListElement[_StackVal], reverse: _StackIterWay = _StackIterWayFalse):
        """
        Initialize new BiDirectionalListValuesIter object
        :param stack: starting point(BiDirectionalListElement)
        :param reverse: reversed iteration(bool)
        """
        ...

    def __iter__(self) -> "BiDirectionalListValuesIter[_StackVal, _StackIterWay]":
        """
        Implementation of iter(metacls)
        :return: metacls
        """
        ...

    def __next__(self) -> _StackVal:
        """
        Implementation of next(metacls)
        :return: current value(Any)
        """
        ...
