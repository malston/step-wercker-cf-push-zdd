import abc

class PipelineStepInterface(object):
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def run(self, **kwargs):
        print "returns a (string, err) tuple"
        return
