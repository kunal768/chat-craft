import { useState } from "react";
import { useRouter } from "next/navigation";

export const Auth = ({type}) => {

    const router = useRouter();
    const [userDetails,setUserDetails] = useState({
        name: "",
        email: "",  
    })

    // async function sendRequest(){
    //     try {
    //         const response = await axios.post(`${BACKEND_URL}/api/v1/user/${type === "signup" ? "signup" : "signin"}`,
    //             postInputs
    //         )
    //         const jwt = response.data.jwt;
    //         localStorage.setItem("token", jwt)
    //         navigate('/blogs')
    //     } catch(e) {
    //         //alert the user
    //     }
    // }
 
    return <div className="bg-white text-black h-screen  flex flex-col justify-center">
        <div className="flex justify-center">
            <div>
                <div className="px-10 text-center">
                    <div className="text-3xl font-extrabold">
                        Create an account
                    </div>
                </div>
                <div className="pt-8">
                    { type === "signup" ? <LabelledInput label="Name" placeholder="Nikhil..." onChange={(e) => {
                        setUserDetails({
                            ...userDetails,
                            name: e.target.value
                        })
                    }} /> : null}
                    <LabelledInput label="Email" placeholder="Nikhil@gmail.com" onChange={(e) => {
                        setUserDetails({
                            ...userDetails,
                            email: e.target.value
                        })
                    }} />
                    <button onClick={()=> {
                        router.push('/dashboard')
                    }} type="button" className="w-full mt-8 text-white cursor-pointer bg-gray-800 hover:bg-gray-900 focus:outline-none focus:ring-4 focus:ring-gray-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-gray-800 dark:hover:bg-gray-700 dark:focus:ring-gray-700 dark:border-gray-700">{type === "signup" ? "Sign up" : "Sign in"}</button>
                </div>
            </div>
        </div>
    </div>
}


function LabelledInput ({label, placeholder,onChange,type}){
    return <div>
    <label className="block mb-2 text-sm font-semibold text-gray-900 pt-4">{label}</label>
    <input onChange={onChange} type={type || "text"} id="first_name" className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5" placeholder={placeholder} required />
</div>  

}
