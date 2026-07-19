function LandingPage({ onStart }) {

    return (

        <div className="landing">

            <div className="landing-card">

                <div className="logo-circle">
                    💬
                </div>

                <h1>TechMart Chat Support</h1>

                <p>
                    Welcome to TechMart AI Support.
                    <br />
                    Get instant assistance with product information,
                    billing, warranty, refunds and technical support.
                </p>

                <button onClick={onStart}>
                    Start New Chat
                </button>

            </div>

        </div>

    );

}

export default LandingPage;