import UIKit
import AVFoundation

class ViewController: UIViewController {
    
    //timer settings
    var counter = 0
    var totalTime = 0
    var titleee = "tit"
    var theTiming = Timer()
    var player: AVAudioPlayer!
    
    //Progress View for countdown
    @IBOutlet weak var countDownSlider: UIProgressView!
    
    //Title Label
    @IBOutlet weak var label: UILabel!
    
    //Libary for egg types
    let timer = ["Az pişmiş": 5 * 60, "Orta pişmiş": 7 * 60, "Tam pişmiş": 12 * 60]

    //Button pressed
    @IBAction func eggButtonPressed(_ sender: UIButton) {
        sender.setTitleColor(.darkGray, for: .normal)
    }
    
    //Button released
    @IBAction func eggButtonReleased(_ sender: UIButton) {
        sender.setTitleColor(.black, for: .normal)
        
        //Reseting
        countDownSlider.progress = 0.0
        counter = 0
        theTiming.invalidate()
        
        titleee = sender.currentTitle!
        let hardness = sender.currentTitle!

        //Setting the count down depending on the selected egg
        totalTime = timer[hardness]! * 100
        
        //Setting the Timer to count down
        theTiming = Timer.scheduledTimer(timeInterval: 0.01, target: self, selector: #selector(updateCounter), userInfo: nil, repeats: true)
    }
    
    //Updating Counter to count backwards while it's bigger than 0
    @objc func updateCounter() {
        //Updating timer
        if counter <= totalTime {
            //debug printer
            print("\(counter / 100) \(totalTime / 100) \(counter/totalTime)")
            //updating progress view
            countDownSlider.progress = Float(counter) / Float(totalTime)
            counter += 1
        } else {
            playAlarm(title: "alarm_sound", extensionOfFile: "mp3")
            theTiming.invalidate()
            label.text = titleee + " YUMURTAN HAZIRDIR da!!"
            
            countDownSlider.progress = 1.0
        }
        
        // Just for graphics - NOT IMPORTANT
        if countDownSlider.progress <= 0.7 && countDownSlider.progress > 0.5 {
            countDownSlider.progressTintColor = .systemYellow
            label.text = titleee + " Hesaplaniyaaa... az kaldi"
        } else if countDownSlider.progress <= 0.5 {
            countDownSlider.progressTintColor = .systemGreen
            label.text = titleee + " Hesaplaniyaaa..."
        } else if countDownSlider.progress > 0.7 && countDownSlider.progress < 0.9 {
            countDownSlider.progressTintColor = .systemRed
            label.text = titleee + " Hesaplaniyaaa... hazir ol da pişti pişecek!"
        }
    }
    
    //Sound Playing
    func playAlarm(title: String, extensionOfFile: String) {
        let url = Bundle.main.url(forResource: title, withExtension: extensionOfFile)
        player = try! AVAudioPlayer(contentsOf: url!)
        player.play()
    }
}
