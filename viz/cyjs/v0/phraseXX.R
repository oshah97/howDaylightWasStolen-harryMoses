library (RCyjs)

#------------------------------------------------------------------------------------------------------------------------
simpleDemoGraph = function ()
{
  g = new ('graphNEL', edgemode='directed')

  nodeDataDefaults(g, attr='type') <- 'undefined'
  nodeDataDefaults(g, attr='lfc') <-  1.0
  nodeDataDefaults(g, attr='label') <- 'default node label'
  nodeDataDefaults(g, attr='count') <-  0

  edgeDataDefaults(g, attr='edgeType') <- 'undefined'
  edgeDataDefaults(g, attr='score') <-  0.0
  edgeDataDefaults(g, attr= 'misc') <- "default misc"

  g = graph::addNode ('A', g)
  g = graph::addNode ('B', g)
  g = graph::addNode ('C', g)
  nodeData (g, 'A', 'type') = 'kinase'
  nodeData (g, 'B', 'type') = 'transcription factor'
  nodeData (g, 'C', 'type') = 'glycoprotein'

  nodeData (g, 'A', 'lfc') = -3.0
  nodeData (g, 'B', 'lfc') = 0.0
  nodeData (g, 'C', 'lfc') = 3.0

  nodeData (g, 'A', 'count') = 2
  nodeData (g, 'B', 'count') = 30
  nodeData (g, 'C', 'count') = 100

  nodeData (g, 'A', 'label') = 'Gene A'
  nodeData (g, 'B', 'label') = 'Gene B'
  nodeData (g, 'C', 'label') = 'Gene C'

  g = graph::addEdge ('A', 'B', g)
  g = graph::addEdge ('B', 'C', g)
  g = graph::addEdge ('C', 'A', g)

  edgeData (g, 'A', 'B', 'edgeType') = 'phosphorylates'
  edgeData (g, 'B', 'C', 'edgeType') = 'synthetic lethal'

  edgeData (g, 'A', 'B', 'score') =  35.0
  edgeData (g, 'B', 'C', 'score') =  -12

  g

} # simpleDemoGraph
#----------------------------------------------------------------------------------------------------
run <- function()
{

   g <- simpleDemoGraph()
   rcy <- RCyjs(portRange=portRange, quiet=TRUE, graph=g, hideEdges=FALSE);

   checkTrue(ready(rcy))

   title <- "demo"
   setBrowserWindowTitle(rcy, title)
   checkEquals(getBrowserWindowTitle(rcy), title)

   tbl.nodes <- getNodes(rcy)
   checkEquals(nrow(tbl.nodes), 3)
   checkEquals(tbl.nodes$name, c("A", "B", "C"))

   setNodeLabelRule(rcy, "label");
   setNodeSizeRule(rcy, "count", c(0, 30, 110), c(20, 50, 100));
   setNodeColorRule(rcy, "count", c(0, 100), c(colors$green, colors$red), mode="interpolate")
   redraw(rcy)
   layout(rcy, "cose")

   rcy

} # run
#------------------------------------------------------------------------------------------------------------------------
