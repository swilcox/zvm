#
# A helper class to access individual bits of a bitfield in a Pythonic
# way.
#
# Inspired from a recipe at:
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/113799
#
# For the license of this file, please consult the LICENSE file in the
# root directory of this distribution.
#

class BitField:
    """An bitfield gives read/write access to the individual bits of a
    value, in array and slice notation.

    Conversion back to an int value is also supported, and a method is
    provided to print the value in binary for debug purposes.

    For all indexes, 0 is the LSB (Least Significant Bit)."""

    def __init__(self, value=0):
        """Initialize a bitfield object from a number or string value."""
        if isinstance(value, str):
            self._d = 0
            for i,v in zip(range(0,8*len(value),8),
                           [ord(s) for s in value[::-1]]):
                self[i:i+8] = v
        else:
            self._d = value

    def __getitem__(self, n):
        """Get the value of a single bit."""
        if isinstance(n, slice):
            start, end = (n.start, n.stop)
            if start > end:
                (start, end) = (end, start)
            mask = 2**(end - start) -1
            return (self._d >> start) & mask
        return (self._d >> n) & 1

    def __setitem__(self, n, value):
        """Set the value of a single bit."""
        if isinstance(n, slice):            
            mask = 2**(n.stop - n.start) - 1
            value = (value & mask) << n.start
            mask = mask << n.start
            self._d = (self._d & ~mask) | value
        else:
            value    = (value & 1) << n
            mask     = 1 << n
            self._d  = (self._d & ~mask) | value

    def __int__(self):
        """Return the whole bitfield as an integer."""
        return self._d

    def to_str(self, len):
        """Print the binary representation of the bitfield."""
        return ''.join(["%d" % self[i]
                        for i in range(len-1,-1,-1)])
