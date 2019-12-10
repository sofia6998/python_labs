import React, {useEffect, useState} from 'react';
import './App.scss';
import RadioButton from "./RadioButton";


const test_values = {
    photoURL: 'https://giantbomb1.cbsistatic.com/uploads/original/0/6087/2437349-pikachu.png',
    variants: ['pikachu', 'raichu', 'psyduck'],
    answer: 'pikachu',
};

const [EASY, MEDIUM, HARD] = ['easy', 'medium', 'hard'];
const levels = [EASY, MEDIUM, HARD];

const [CORRECT, WRONG, EMPTY] = ['Correct!', 'Wrong!', null];
function App() {
    const [question, setQuestion] = useState(test_values);
    const [selectedOption, setSelectedOption] = useState(null);
    const [result, setResult] = useState(EMPTY);
    const [level, setLevel] = useState(EASY);

    useEffect(() => { getNewQuestion() }, [level]);

    const getNewQuestion = async () => {
        let gameInfo = null;
        try {
            gameInfo = await getJson(`/api?level=${level}`);
            const {photo, answer, variants} = gameInfo;
            setQuestion({
                photoURL: photo,
                variants,
                answer
            });
        } catch (e) {
            console.log(e);
            gameInfo = { error: e };
        }
    };

    const selectOption = (option) => {
        setSelectedOption(option);
    };

    const checkAnswer = () => {
        console.log(selectedOption);
        const newResult = selectedOption === question.answer
            ? CORRECT
            : WRONG;
        setResult(newResult);
    };

    const getNextQuestion = () => {
        setResult(EMPTY);
        setSelectedOption(null);
        getNewQuestion();
    };

      return (
        <div className="App">
            <RadioButton options={levels} selected={level} onSelect={setLevel}/>
            <img src={question.photoURL} className="App-logo" alt="logo" />
            <div className={'selectWrapper'}>
                <span className={'label'}>This is </span>
                <DropDown onSelect={selectOption}
                          selected={selectedOption}
                          variants={question.variants || []}/>
                {selectedOption && <button className={'brk-btn submitButton'} onClick={checkAnswer}>check</button>}
            </div>
            {result && <div>{result}</div>}
            {result && <button className={'brk-btn nextButton'} onClick={getNextQuestion}>next</button>}
        </div>
      );
}

const DropDown = (props) => {
    const {onSelect, selected, variants} = props;
    const [isOpen, setIsOpen] = useState(false);
    const handleSelect = (el) => {
        setIsOpen(false);
        onSelect(el);
    };
    const sortedVariants = variants.sort((a, b) => a === selected ? -1 : 1);
    return <span className={'selectWrapper'}>
                    <button className={'placeholder'} onClick={() => setIsOpen(!isOpen)}>{selected || '      '}</button>
                    <span className={`list ${isOpen ? 'visible' : ''}`}>
                        {sortedVariants.map((el, i) =>
                            <button key={i} className="variants" onClick={() => handleSelect(el)}>{el}</button>
                        )}
                    </span>
                </span>;
};

const getJson = async (input) => {
    const response = await fetch(input, {
        method: 'GET'
    });
    return response.json();
};


export default App;
