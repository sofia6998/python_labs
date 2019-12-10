import React, {useEffect, useState} from 'react';
import "./RadioButton.scss";

export default function RadioButton(props) {
    const {options, selected, onSelect} = props;
    console.log("options", options);
    return(
        <div className="rb">
            {options && options.map((el) =>
                <div onClick={() => onSelect(el)}
                     className={`rb-tab ${selected === el ? 'rb-tab-active' : ''}`} key={el} data-value={el}>
                <div className="rb-spot">
                    <span className="rb-txt">{el}</span>
                </div>
            </div>
            )}
        </div>
    );
}