function System() {
    return (
        <div className="space-y-8">
            <div>
                <h1 className="text-3xl font-bold text-gray-900">
                    System
                </h1>
                <p className="mt-2 text-gray-500">
                    Monitor the weather pipeline and application status.
                </p>
            </div>

            <section>
                <h2 className="text-xl font-semibold text-gray-900">
                    System Status
                </h2>
                <div className="mt-4 rounded-xl border bg-white p-6">
                    <p className="text-gray-500">
                        System information will appear here.
                    </p>
                </div>
            </section>
        </div>
    )
}

export default System