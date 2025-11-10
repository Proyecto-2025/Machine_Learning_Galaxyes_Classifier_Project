import { useState,React } from "react"

export default function(){
    const [form,updateForm] = useState(
        {
            nickname:"",
            password:""
        }
    );

    const handleChange = (event) => {
        console.log(event);
        const {name, value } = event.target;
    }
    return(
        <div>
            <form>
                <input type="text" nickname="nickname"/>
                <input type="password" name="password" />
            </form>
        </div>
    )    
    
}