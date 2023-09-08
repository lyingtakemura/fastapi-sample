import { useState } from "react";

export function Alert(props) {
    const [visible, setVisible] = useState(true);

    function handleClick() {
        return setVisible(!visible);
    }

    return (
        <div>
            <button onClick={handleClick}>test</button>
            {visible && <h1>{props.message}</h1>}
        </div>
    );
}
