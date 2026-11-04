class Solution(object):
    def hIndex(self, citations):
        """
        :type citations: List[int]
        :rtype: int
        """
        citations.sort()
        leng = len(citations)
        for i, val in enumerate(citations):
            if val >= (leng - i):
                return leng - i
        return 0
