from agents import build_reader_agent, build_search_agent, writer_chain,critic_chain

def run_research_pipeline(topic:str) -> dict:

    state={}

    # search agent working

    print("\n"+" = "*50)

    print("step 1- search agent is working...")

    print("="*50)

    search_agent=build_search_agent()

    # provide messages as list of dicts with role and content
    search_result=search_agent.invoke({
        "messages": [
            {"role": "user", "content": f"Find recent, reliable and detailed information on the topic: {topic}"}
        ]
    })

    state["search_result"]=search_result['messages'][-1].content

    print("\n search result ",state["search_result"])


    #Step 2- reader agent

    print("\n"+" = "*50)
    
    print("step 2- reader agent is scraping top resources...")
    
    print("="*50)

    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": (
                    f"Based on the following search results about '{topic}', "
                    f"pick the most relevant URL and scrape it for deeper content.\n\n"
                    f"Search Results:\n{state['search_result'][:800]}"
                ),
            }
        ]
    })

    state['scraped_content'] = reader_result["messages"][-1].content

    print("\n scraped content ",state["scraped_content"][:800])

    #step 3- writer chain

    print("\n"+" = "*50)
        
    print("step 3- writer chain is generating the report...")
        
    print("="*50)

    research_combined=(
        f"Search Results:\n{state['search_result']}\n\n"
        f"Scraped Content:\n{state['scraped_content']}"
    )

    state['report']=writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })

    print("\n Final Report Generated:\n",state['report'])

    # Step 4- Critic report

    print("\n"+" = "*50)
            
    print("step 4- critic chain is reviewing the report...")
            
    print("="*50)

    state['feedback']=critic_chain.invoke({
        "report": state['report']
    })

    print("\n Critic Feedback:\n",state['feedback'])

    return state

if __name__ == "__main__":
    topic=input(" \n Enter the research topic: ")
    run_research_pipeline(topic)






    