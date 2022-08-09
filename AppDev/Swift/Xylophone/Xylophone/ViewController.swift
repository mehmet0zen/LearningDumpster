import UIKit
import AVFoundation

class ViewController: UIViewController {
    
    var player: AVAudioPlayer!

    override func viewDidLoad() {
        super.viewDidLoad()
    }

    @IBAction func keyPressed(_ sender: UIButton) {
        
        playSound(title: sender.currentTitle!, extensionOfFile: "wav")
        sender.alpha = 0.5
    }
    
    @IBAction func keyReleased(_ sender: UIButton) {
        do {
            sleep(UInt32(0.2))
        }
        sender.alpha = 1
    }
    
    func playSound(title: String, extensionOfFile: String) {
        let url = Bundle.main.url(forResource: title, withExtension: extensionOfFile)
        player = try! AVAudioPlayer(contentsOf: url!)
        player.play()
    }
}


