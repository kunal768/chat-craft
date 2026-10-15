export const Quote = () => {
    return <div className="bg-[url('/bg.jpg')] bg-cover bg-center text-black h-screen flex justify-center flex-col" >
        <div className="flex justify-center">
            <div className="flex justify-center">
                <div className="h-[500px] w-[500px] bg-[url('/logo.png')] bg-cover bg-center "></div>
                <div className="flex flex-col justify-center">
                    <div className="text-4xl text-white font-bold">
                    Chat-Craft
                    </div>
                    <div className="max-w-md text-white text-2xl font-semibold mt-4">
                    Transform your customer support experience with AI that understands, learns, and evolves with your business needs.
                    </div>
                    <div className="max-w-md text-sm font-light mt-4 text-white">
                    Join thousands of businesses that have improved customer satisfaction by 85% and reduced response times by 75%.
                    </div>
                </div>
            </div>
        </div>
    </div>
}