The objective here is to port [this](https://github.com/atlarge-research/wta-sim/tree/tasks-across-machines) to [this](https://github.com/atlarge-research/opendc)
# Some notes of how the porting will commence
LookAheadPlacement is the main point of novelty, which is a [TaskPlacementPolicy]()

# OpenDC notes:
### WorkflowServiceImpl
*Job* is a piece of work for OpenDC, in this case it is a single workflow.
Dependencies are contained within workflows

The test creates four hosts with certain specs and the Workflow service creates virtual machines
`WorkflowServiceTest.kt:84 & :129`

The test uses `FilterScheduler` to choose which Host to place a given VM on. This filter has no notion of a runtime, as we are on the VM level, not the task level (But a VM 1-1 Task though??). It allows you to do arbritrary operations on metadata of the VMs to create a "best fit".

What about `WORKFLOW_TASK_DEADLINE` though? idk yet.

The test calls a `replay` function that it implements itself. This is different from the 'replaying' that the ReplayScheduler does. The ReplayScheduler takes a VM assignment input file (real world ex.) that it then actually replays through the VM to host scheduling.

### Trace stuff
* `byName` in `TraceFormat` determines which trace format loader to create
* gwf uses `TASK_WORKFLOW_ID`
* Parquet seems to be just a encapsulating trace format around other stuff, don't have evidence though

# wta-sim notes:
ClusterManager.kt has machines sorted by power efficiency, when scheduling a task in LookAhead it gets the most efficient machine avail.
`Machine.kt` `HostSpec.kt`:
`powerEfficiency = (TDP.toDouble() / numberOfCpus) * normalizedSpeed` `dvfs`

OpenDC has no notion of TDP, normalizedspeed (just a normalization of all the baseclocks) or power effiency.
Add something in NewFlavor.

TASK_WORKFLOW_ID 
