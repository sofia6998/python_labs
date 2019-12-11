import React, {useEffect, useState} from 'react';
import './App.scss';


const ITEMS_PER_PAGE = 5;

function App() {
    const [channels, setChannels] = useState([]);
    const [selectedChanel, setSelectedChanel] = useState({});
    const [currentPage, setCurrentPage] = useState(0);
    const [articles, setArticles] = useState(null);
    const [showCreatePopup, setShowCreatePopup] = useState(false);

    useEffect(() => {
        getChannels();
        }, []);

    useEffect(() => {
        fetchArticles();
    }, [currentPage, selectedChanel]);

    const getChannels = async () => {
        try {
            const result = await getJson('/api?event=getlist');
            setChannels(result);
        } catch (e) {
            console.error(e);
        }
    };

    const selectChanel = async (chanel) => {
        setArticles([]);
        setCurrentPage(0);
        setSelectedChanel(chanel);
    };

    const fetchArticles = async () => {
        try {
            const result = await getJson(`/api?event=getarticles` +
                `&name=${encodeURIComponent('' + selectedChanel)}` +
                `&offset=${encodeURIComponent(currentPage * ITEMS_PER_PAGE)}` +
                `&limit=${encodeURIComponent(ITEMS_PER_PAGE)}`
            );
            console.log('articles:', result);
            if(articles.error) {
                console.error(articles.error);
            } else {
             setArticles(result);
            }
            setShowCreatePopup(false);
        } catch (e) {
            console.error(e);
        }
    };
    const addChanel = async () => {
        const name = document.getElementById("nameInput").value;
        const url = document.getElementById("urlInput").value;
        // todo validate
        if(name && url) {
            try {
                const result = await getJson(`/api?event=add` +
                    `&name=${encodeURIComponent(name)}` +
                    `&url=${encodeURIComponent(url)}`
                );
                console.log('channels:', result);
                setChannels([...Object.values(result)]);
                setShowCreatePopup(false);
            } catch (e) {
                console.error(e);
            }
        }
    };

      return (
        <div className="App">
            <div className="leftBar">
                {channels && channels.map((el, i) => {
                    return (
                        <button key={i} className="chanelItem" onClick={() => selectChanel(el)}>
                            {el}
                        </button>
                    );
                })}
                <button className={'brk-btn'} onClick={() => setShowCreatePopup(true)}> + </button>
            </div>
            {showCreatePopup && <div className="overlayPopup">
                <div>Name</div>
                <input id="nameInput"/>
                <div>Link</div>
                <input id="urlInput"/>
                <button className={'brk-btn addChanelButton'}  onClick={addChanel}>add new channel</button>
            </div>}
            <div className="articlesListWrapper">
                <button disabled={currentPage < 1} className={'brk-btn paginationButton'} onClick={() => setCurrentPage(currentPage - 1)}>
                    prev
                </button>
                <div className="articlesList">
                    {articles && articles.map((el, i) => {
                        return(
                            <div key={i} className="articleWrapper">
                                <div className="articleName">{el.name}</div>
                                <a className="articleURL" href={el.url}>link</a>
                            </div>
                        );
                    })}
                </div>
                <button className={'brk-btn paginationButton'} onClick={() => setCurrentPage(currentPage + 1)}>
                    next
                </button>
            </div>
        </div>
      );
}

const getJson = async (query) => {
    const response = await fetch(query, {
        method: 'GET'
    });
    return response.json();
};

export default App;
