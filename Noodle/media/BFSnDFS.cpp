#include<iostream>
#include<stdlib.h>
using namespace std;
vector<int> adj[100];//adjacent list
bool visited[100];
void GenRandomGraphs(int NOEdge, int NOVertex)
{
   int i, j, edge[NOEdge][2], count;
   i = 0;
   //Assign random values to the number of vertex and edges
   of the graph, Using rand().
   while(i < NOEdge)
   {
      edge[i][0] = rand()%NOVertex+1;
      edge[i][1] = rand()%NOVertex+1;
      //Print the connections of each vertex, irrespective of
      the direction.
      if(edge[i][0] == edge[i][1])
         continue;
      else
      {
         for(j = 0; j < i; j++)
         {
            if((edge[i][0] == edge[j][0] &&
            edge[i][1] == edge[j][1]) || (edge[i][0] == edge[j][1] &&
            edge[i][1] == edge[j][0]))
            i--;
         }
      }i
      ++;
   }
   cout<<"\nThe generated random graph is: ";
   for(i = 0; i < NOVertex; i++)
   {
      count = 0;
      cout<<"\n\t"<<i+1<<"-> { ";
      for(j = 0; j < NOEdge; j++)
      {
         if(edge[j][0] == i+1)
         {
            cout<<edge[j][1]<<" ";
            adj[i].push_back(edge[j][1]);
            count++;
         } else if(edge[j][1] == i+1)
         {
            cout<<edge[j][0]<<" ";
            adj[i].push_back(edge[j][0]);
            count++;
         } else if(j== NOEdge-1 && count == 0)
         cout<<"Isolated Vertex!"; //Print “Isolated vertex” for the vertex having no degree.
      }
      cout<<" }";
   }
}
void BFS(){
queue<int> q;
    q.push(0);
    int prev[(n-1)*(m-1)];
    for(int i=0;i<(n-1)*(m-1);i++){visited[i]=false;prev[i]=-1;}
    visited[0]=true;
    while(!q.empty()){
        int node=q.front();
        q.pop();
        for(auto i=adj[node].begin();i!=adj[node].end();i++){
            if(!visited[*i]){q.push(*i);visited[*i]=true;prev[*i]=node;}
        }
    }

}
int main()
{
   int i, e, n;//e edges and n vertices, e= N*2, n=N, N = 6,7,8,9,10
   cout<<"Random graph generation: ";
   n= 6 + rand()%5;
   e = 2*n;
   GenRandomGraphs(e, n);
}
